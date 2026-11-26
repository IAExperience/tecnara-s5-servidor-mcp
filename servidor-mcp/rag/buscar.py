"""Búsqueda híbrida sobre indice.json: BM25 (palabras) + embeddings (significado), juntadas con RRF.

Uso (dentro de servidor-mcp/):
    uv run rag/buscar.py "¿qué hace el formulario de contacto?"
    uv run rag/buscar.py "FR-003" --solo-bm25          (o --solo-vectores, para comparar)

Si no encuentra nada que se parezca, devuelve una lista vacía: así el RAG puede decir «no lo sé».
"""
import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from indexar import INDICE, embeber  # noqa: E402

UMBRAL = 0.70   # similitud mínima para que un trozo cuente como «parecido» (Gemini Embedding 2: con respuesta ≈0,73–0,79; sin ella ≈0,55–0,67). Ajustadlo con vuestras preguntas
# Palabras que salen en casi todo y no ayudan a encontrar nada
VACIAS = set("de la el los las un una unos unas y o en que por para con sin del al se es lo le su sus mi "
             "como cual cuanto cuanta cuantos que quien donde cuando hay tiene hace esta este esto".split())


def rrf(listas: list[list[str]], k: int = 60) -> list[str]:
    """Reciprocal Rank Fusion: junta varias listas ordenadas en una sola.

    listas: una lista de ids por buscador, la mejor primero. Ejemplo: [["a", "b"], ["b", "c"]]
    Cada id suma 1 / (k + puesto) en cada lista donde aparece. El puesto empieza en 1.
    Devuelve los ids ordenados de más a menos puntos.
    """
    # TODO (vosotros): cinco líneas, sin Claude. Comprobad con: uv run rag/test_rrf.py
    raise NotImplementedError("Escribid rrf() en rag/buscar.py")


def palabras(texto: str) -> list[str]:
    """Minúsculas, sin tildes, y troceado en palabras y números (FR-003 → fr, 003)."""
    t = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return [w for w in re.findall(r"[a-z0-9]+", t) if (len(w) > 1 or w.isdigit()) and w not in VACIAS]


def bm25(pregunta: str, trozos: list[dict], k1: float = 1.5, b: float = 0.75) -> list[str]:
    """Ids de los trozos que contienen alguna palabra de la pregunta, el mejor primero (como en el curso)."""
    docs = [palabras(t["texto"]) for t in trozos]
    media = sum(map(len, docs)) / len(docs)
    df = Counter(w for d in docs for w in set(d))
    puntos = {}
    for t, d in zip(trozos, docs):
        tf = Counter(d)
        s = sum(math.log(1 + (len(docs) - df[w] + .5) / (df[w] + .5)) * tf[w] * (k1 + 1)
                / (tf[w] + k1 * (1 - b + b * len(d) / media)) for w in set(palabras(pregunta)) if w in tf)
        if s > 0:
            puntos[t["cita"]] = s
    return sorted(puntos, key=puntos.get, reverse=True)


def vectores(pregunta: str, trozos: list[dict]) -> list[str]:
    """Ids de los trozos con similitud del coseno ≥ UMBRAL, el más parecido primero."""
    if not trozos or trozos[0]["vector"] is None:
        return []
    q = embeber([pregunta], "pregunta")[0]
    nq = math.sqrt(sum(x * x for x in q))
    sim = {}
    for t in trozos:
        v = t["vector"]
        s = sum(x * y for x, y in zip(q, v)) / (nq * math.sqrt(sum(y * y for y in v)))
        if s >= UMBRAL:
            sim[t["cita"]] = s
    return sorted(sim, key=sim.get, reverse=True)


def buscar(pregunta: str, modo: str = "hibrida", tope: int = 4) -> list[dict]:
    """Los trozos más relevantes (como mucho «tope»), cada uno con su cita archivo#encabezado."""
    trozos = json.loads(INDICE.read_text(encoding="utf-8"))["trozos"]
    por_cita = {t["cita"]: t for t in trozos}
    if modo == "bm25":
        ids = bm25(pregunta, trozos)
    elif modo == "vectores":
        ids = vectores(pregunta, trozos)
    else:
        ids = rrf([bm25(pregunta, trozos), vectores(pregunta, trozos)])
    return [{"cita": i, "texto": por_cita[i]["texto"]} for i in ids[:tope]]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("pregunta")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--solo-bm25", action="store_const", dest="modo", const="bm25")
    g.add_argument("--solo-vectores", action="store_const", dest="modo", const="vectores")
    a = p.parse_args()
    encontrados = buscar(a.pregunta, a.modo or "hibrida")
    if not encontrados:
        print("No está en la documentación del proyecto.")
    for t in encontrados:
        print(f"\n[{t['cita']}]\n{t['texto'][:300]}")
