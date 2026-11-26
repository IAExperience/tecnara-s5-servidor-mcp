"""Paso de preparación del RAG: trocea los .md por encabezados, calcula los embeddings y guarda indice.json.

Uso (dentro de servidor-mcp/):
    uv run rag/indexar.py --carpetas ../specs ../docs
    uv run rag/indexar.py --carpetas ../specs --solo-bm25      (sin embeddings ni claves)

Se hace una vez, y otra cada vez que cambien los documentos. Cada pregunta solo lee indice.json.
"""
import argparse
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent           # servidor-mcp/
INDICE = RAIZ / "indice.json"
LOTE = 50                                                 # trozos por llamada: pocas llamadas, sin pasar del límite gratuito
load_dotenv(RAIZ / ".env")


def trocear(texto: str, archivo: str) -> list[dict]:
    """Un trozo por encabezado (#, ##, ###…). La cita es archivo#encabezado."""
    trozos, titulo, lineas = [], "inicio", []

    def cerrar():
        cuerpo = "\n".join(lineas).strip()
        if cuerpo:
            trozos.append({"cita": f"{archivo}#{titulo}", "texto": f"{titulo}\n{cuerpo}"})

    for linea in texto.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)", linea)
        if m:
            cerrar()
            titulo, lineas = m.group(1).strip(), []
        else:
            lineas.append(linea)
    cerrar()
    return trozos


def embeber(textos: list[str], tipo: str) -> list[list[float]]:
    """tipo: 'documento' al indexar, 'pregunta' al buscar. Proveedor según EMBEDDINGS en .env."""
    proveedor = os.getenv("EMBEDDINGS", "ninguno")
    vectores = []
    for i in range(0, len(textos), LOTE):
        lote = textos[i:i + LOTE]
        if proveedor == "gemini":
            from google import genai
            from google.genai import types
            # Gemini Embedding 2 no usa task_type: el tipo va como prefijo en el propio texto.
            # Cada texto en su propio Content: una lista de textos sueltos daría UN solo vector para todos.
            prefijo = (lambda t: f"title: {t.split(chr(10), 1)[0]} | text: {t}") if tipo == "documento" \
                else (lambda t: f"task: search result | query: {t}")
            cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # en variable: si no, se cierra antes de la llamada
            r = cliente.models.embed_content(
                model="gemini-embedding-2",
                contents=[types.Content(parts=[types.Part.from_text(text=prefijo(t))]) for t in lote],
                config=types.EmbedContentConfig(output_dimensionality=768))
            vectores += [e.values for e in r.embeddings]
        elif proveedor == "voyage":
            import voyageai
            r = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY")).embed(
                lote, model="voyage-3-large", input_type="document" if tipo == "documento" else "query")
            vectores += r.embeddings
        else:
            raise SystemExit(f"EMBEDDINGS={proveedor!r}: pon gemini o voyage en .env, o usa --solo-bm25")
    return vectores


def main():
    p = argparse.ArgumentParser(description="Crea indice.json a partir de los .md de las carpetas")
    p.add_argument("--carpetas", nargs="+", default=["../specs", "../docs"])
    p.add_argument("--solo-bm25", action="store_true", help="sin embeddings: solo búsqueda por palabras")
    a = p.parse_args()

    trozos = []
    for carpeta in a.carpetas:
        base = (RAIZ / carpeta).resolve()
        for f in sorted(base.rglob("*.md")):
            trozos += trocear(f.read_text(encoding="utf-8"), f.relative_to(base.parent).as_posix())
    if not trozos:
        raise SystemExit(f"No hay ningún .md en {a.carpetas}")

    vectores = None if a.solo_bm25 else embeber([t["texto"] for t in trozos], "documento")
    for i, t in enumerate(trozos):
        t["vector"] = vectores[i] if vectores else None

    INDICE.write_text(json.dumps({"embeddings": None if a.solo_bm25 else os.getenv("EMBEDDINGS"), "trozos": trozos},
                                 ensure_ascii=False), encoding="utf-8")
    print(f"indice.json: {len(trozos)} trozos de {len({t['cita'].split('#')[0] for t in trozos})} archivos"
          + (" (solo BM25)" if a.solo_bm25 else f" con embeddings de {os.getenv('EMBEDDINGS')}"))


if __name__ == "__main__":
    main()
