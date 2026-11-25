"""Comprueba vuestra rrf().   uv run rag/test_rrf.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from buscar import rrf  # noqa: E402

# «b» sale 2.º y 1.º: suma más que «a» (1.º en una sola lista)
assert rrf([["a", "b"], ["b", "c"]]) == ["b", "a", "c"], rrf([["a", "b"], ["b", "c"]])
# Una sola lista: el orden no cambia
assert rrf([["x", "y", "z"]]) == ["x", "y", "z"]
# Listas vacías: nada (así el RAG puede decir «no lo sé»)
assert rrf([[], []]) == []
print("rrf() correcta")
