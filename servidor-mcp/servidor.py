"""Servidor MCP de ejemplo, como el del curso oficial (Building with the Claude API, «Model Context Protocol»).

Trae una pieza de cada primitiva sobre unos documentos de ejemplo:
  - tools     → leer_doc y editar_doc   (las usa Claude cuando decide)
  - resources → docs://lista y docs://{nombre}   (datos que se leen)
  - prompt    → resumir   (un flujo que lanzas tú)

Práctica 1: adaptarlo a vuestra startup (listar_equipo, actualizar_bio, startup://equipo/{slug}, escribir_bio).
Práctica 2: añadirle la tool buscar_docs, que usa rag/buscar.py.

Probarlo:   uv run mcp dev servidor.py        (abre el MCP Inspector)
"""
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("startup", log_level="ERROR")

# Documentos de ejemplo, en memoria. En la práctica 1 los cambiáis por las fichas de equipo/.
docs = {
    "bienvenida.md": "Cierzo Labs hace webs para comercios de barrio en Zaragoza.",
    "precios.md": "Plan básico: 300 euros. Plan con tienda: 900 euros.",
}


@mcp.tool(name="leer_doc", description="Lee un documento de la startup y devuelve su texto.")
def leer_doc(nombre: str = Field(description="Nombre del documento, por ejemplo bienvenida.md")) -> str:
    if nombre not in docs:
        raise ValueError(f"No existe el documento {nombre}")
    return docs[nombre]


@mcp.tool(name="editar_doc", description="Cambia un texto exacto de un documento por otro. Lee el documento antes.")
def editar_doc(
    nombre: str = Field(description="Nombre del documento"),
    texto_viejo: str = Field(description="Texto que se reemplaza; tiene que estar tal cual, con espacios incluidos"),
    texto_nuevo: str = Field(description="Texto nuevo"),
) -> str:
    if nombre not in docs:
        raise ValueError(f"No existe el documento {nombre}")
    if texto_viejo not in docs[nombre]:
        raise ValueError(f"El texto a reemplazar no está en {nombre}: léelo primero")
    docs[nombre] = docs[nombre].replace(texto_viejo, texto_nuevo)
    return "Hecho"


@mcp.resource("docs://lista", mime_type="application/json")
def lista_docs() -> list[str]:
    return list(docs)


@mcp.resource("docs://{nombre}", mime_type="text/plain")
def doc(nombre: str) -> str:
    if nombre not in docs:
        raise ValueError(f"No existe el documento {nombre}")
    return docs[nombre]


@mcp.prompt(name="resumir", description="Resume un documento en tres frases.")
def resumir(nombre: str = Field(description="Nombre del documento")) -> list[base.Message]:
    return [base.UserMessage(f"Lee el documento {nombre} con la tool leer_doc y resúmelo en tres frases.")]


if __name__ == "__main__":
    mcp.run(transport="stdio")
