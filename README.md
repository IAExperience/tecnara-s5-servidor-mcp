# Scaffold de la sesión 5 · MCP y RAG

Curso *Construye con IA* (IA Experience · Tecnara).

Una carpeta, `servidor-mcp/`, que se integra en el repo de vuestra startup: un servidor MCP de ejemplo y las piezas de un RAG, en Python con uv.

## Cómo se usa

En Claude Code, dentro del repo de vuestra startup, escribid:

```text
Integra el scaffold de https://github.com/IAExperience/tecnara-s5-servidor-mcp en nuestro repo siguiendo su servidor-mcp/INTEGRAR.md
```

Claude lo copia a vuestro repo sin tocar vuestra web. Lo demás se hace en clase.

## Qué hay dentro

- `servidor-mcp/servidor.py`: servidor MCP de ejemplo (tools, resources y un prompt). En la práctica 1 lo adaptáis a vuestra startup.
- `servidor-mcp/rag/`: indexar, buscar y preguntar con citas. En la práctica 2 escribís la función `rrf()`.
- `servidor-mcp/ejemplo/`: specs inventados de una startup ficticia, para probar, y `web/index.html`, un formulario de contacto que avisa a un webhook de n8n (la demo del formador).

Las claves van en `servidor-mcp/.env`, que nunca se sube a GitHub.
- `skills/prompt-mejorado/`: un regalo de Alessandro, la skill que convierte ideas sueltas en un prompt profesional. Para instalarla, pedídselo a Claude Code con el prompt de la sesión.
