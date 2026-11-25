"""El paso final del RAG: busca los trozos y le pide a Claude que responda SOLO con ellos, citando.

Uso (dentro de servidor-mcp/):
    uv run rag/preguntar.py "¿qué hace el formulario de contacto?"
    uv run rag/preguntar.py "¿cuánto cobra la startup?" --solo-bm25
"""
import argparse
import os
import sys
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from buscar import buscar  # noqa: E402  (importa indexar, que carga el .env)

MODELO = "claude-haiku-5-5"   # el más barato: para responder con 4 trozos sobra


def preguntar(pregunta: str, modo: str = "hibrida") -> str:
    trozos = buscar(pregunta, modo)
    if not trozos:
        return "No está en la documentación del proyecto."   # «no lo sé», sin gastar ni una llamada
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit("Falta ANTHROPIC_API_KEY en servidor-mcp/.env (la da el formador)")

    # Cada trozo va como un documento con las citas activadas: Claude dice de cuál sale cada frase
    documentos = [{"type": "document", "title": t["cita"], "citations": {"enabled": True},
                   "source": {"type": "text", "media_type": "text/plain", "data": t["texto"]}} for t in trozos]
    r = anthropic.Anthropic().messages.create(
        model=MODELO, max_tokens=2000, output_config={"effort": "low"},
        system="Responde en español y SOLO con lo que digan los documentos. "
               "Si no lo dicen, responde exactamente: «No está en la documentación del proyecto». "
               "Si la pregunta es ambigua, dilo y separa las posibles respuestas.",
        messages=[{"role": "user", "content": documentos + [{"type": "text", "text": pregunta}]}],
    )
    if r.stop_reason == "refusal":
        return "Claude no ha querido responder a esta pregunta."

    salida, citas = "", []
    for bloque in r.content:
        if bloque.type != "text":
            continue
        salida += bloque.text
        for c in bloque.citations or []:
            if c.document_title not in citas:
                citas.append(c.document_title)
            salida += f" [{citas.index(c.document_title) + 1}]"
    return salida + "".join(f"\n[{i}] {c}" for i, c in enumerate(citas, 1))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("pregunta")
    p.add_argument("--solo-bm25", action="store_const", dest="modo", const="bm25", default="hibrida")
    a = p.parse_args()
    print(preguntar(a.pregunta, a.modo))
