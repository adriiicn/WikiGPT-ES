from dataclasses import dataclass
from typing import Iterable

from wikigpt_es.indexer import WikiIndex, score_query


@dataclass(frozen=True)
class ChatResponse:
    answer: str
    sources: list[str]


class TriadaVGChatbot:
    """
    Arquitectura TRIADA-VG:
    1) Recuperación: busca pasajes con TF-IDF sobre artículos de videojuegos.
    2) Inferencia: sintetiza una respuesta breve con heurísticas controladas.
    3) Anclaje: conserva títulos de artículos usados como fuentes.
    """

    def __init__(self, index: WikiIndex) -> None:
        self.index = index

    def answer(self, question: str) -> ChatResponse:
        results = score_query(self.index, question, top_k=5)
        if not results:
            return ChatResponse(
                answer=(
                    "No encontré un artículo relevante dentro de la categoría de videojuegos. "
                    "Prueba con otro título o palabra clave."
                ),
                sources=[],
            )

        synthesis = self._synthesize_answer(question, results)
        sources = [item["title"] for item in results]
        return ChatResponse(answer=synthesis, sources=sources)

    def _synthesize_answer(self, question: str, results: Iterable[dict]) -> str:
        question = question.strip()
        snippets = []
        for entry in results:
            summary = entry.get("summary", "").strip()
            if summary:
                snippets.append(summary)
            if len(snippets) >= 3:
                break

        if not snippets:
            return "No hay suficiente información en los artículos recuperados."

        joined = " ".join(snippets)
        answer = (
            f"Pregunta: {question}\n"
            "Respuesta basada en Wikipedia (videojuegos): "
            f"{joined}"
        )
        return answer
