# Integrar el scaffold `servidor-mcp/` en el repo de la startup

**Para Claude Code.** El equipo te pedirá algo como: «Integra el scaffold de `<ruta o url>` en nuestro repo siguiendo su INTEGRAR.md». Sigue estos pasos en orden, enseña el plan antes de tocar nada y no hagas nada más.

## Qué es

Una carpeta autocontenida (Python, con uv) con un servidor MCP de ejemplo y las piezas de un RAG. Se usa en la sesión 5 del curso:
- **Práctica 1:** el equipo adapta `servidor.py` a su startup.
- **Práctica 2:** el equipo indexa su documentación y añade la tool `buscar_docs`.

**No la adaptes tú ahora:** eso lo hacen ellos en las prácticas.

## Reglas

- **No toques la web.** Ni sus HTML, CSS y JS, ni su `package.json` o sus dependencias si las tiene. El scaffold vive aparte, en `servidor-mcp/`, con sus propias dependencias.
- **Nunca leas ni muestres un `.env`.** Si hace falta crearlo, cópialo de `.env.example` y deja que el equipo pegue las claves.
- Si algo del repo no encaja con estos pasos (ya existe una carpeta `servidor-mcp/`, no hay `specs/`…), para y pregunta.

## Pasos

1. **Copia la carpeta** `servidor-mcp/` a la raíz del repo, tal cual, con `ejemplo/` incluida: sirve para probar.
2. **`.gitignore` de la raíz:** añade estas dos líneas si no están ya:
   ```
   servidor-mcp/.env
   servidor-mcp/.venv/
   ```
3. **Instala:** en la terminal, dentro de `servidor-mcp/`, ejecuta `uv sync`.
4. **Claves:** copia `.env.example` como `.env` (dentro de `servidor-mcp/`). No lo abras: el equipo pega las claves.
5. **Comprueba que funciona sin claves**, dentro de `servidor-mcp/`:
   ```
   uv run rag/indexar.py --carpetas ejemplo/specs ejemplo/docs --solo-bm25
   uv run rag/buscar.py "FR-003" --solo-bm25
   ```
   El primero crea `indice.json` y el segundo tiene que devolver el trozo del formulario de contacto. **Borra después `indice.json`:** el bueno se crea en la práctica 2 con los specs del equipo.
6. **Dónde están sus specs:** busca en el repo las carpetas que dejó Spec Kit (`specs/`, `.specify/`, `docs/`) y díselas al equipo. Son las que indexarán en la práctica 2.
7. **Resume** al equipo qué has hecho en tres líneas y recuérdale:
   - el Inspector se abre con `uv run mcp dev servidor.py` (dentro de `servidor-mcp/`);
   - `rag/buscar.py` tiene la función `rrf()` vacía a propósito: la escriben ellos.

## Si el repo usa algo distinto

- **La web usa un framework o un bundler** (Vite, React…): no cambia nada. `servidor-mcp/` es independiente; solo comprueba que el bundler no intente procesar `servidor-mcp/`. Si lo hace, exclúyelo en su configuración y avisa al equipo.
- **No tienen la CLI `claude`** (solo la extensión de VS Code): copia `mcp.json.ejemplo` a la raíz del repo como `.mcp.json`. Claude Code lo leerá al reiniciar.
