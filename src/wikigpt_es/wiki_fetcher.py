from collections import deque
from dataclasses import dataclass
from typing import Iterable

import wikipediaapi


@dataclass(frozen=True)
class WikiArticle:
    title: str
    summary: str
    text: str


class WikipediaVideoGameFetcher:
    def __init__(self, language: str) -> None:
        self._wiki = wikipediaapi.Wikipedia(language=language, extract_format=wikipediaapi.ExtractFormat.WIKI)

    def iter_video_game_articles(
        self,
        root_category: str,
        max_pages: int,
        max_depth: int,
        min_text_length: int,
    ) -> Iterable[WikiArticle]:
        visited_categories: set[str] = set()
        visited_pages: set[str] = set()
        queue: deque[tuple[str, int]] = deque([(root_category, 0)])
        collected = 0

        while queue and collected < max_pages:
            category_title, depth = queue.popleft()
            if category_title in visited_categories or depth > max_depth:
                continue
            visited_categories.add(category_title)

            category_page = self._wiki.page(category_title)
            for title, member in category_page.categorymembers.items():
                if collected >= max_pages:
                    break

                if member.ns == wikipediaapi.Namespace.CATEGORY and depth < max_depth:
                    if title not in visited_categories:
                        queue.append((title, depth + 1))
                    continue

                if member.ns != wikipediaapi.Namespace.MAIN:
                    continue

                if title in visited_pages:
                    continue

                page = self._wiki.page(title)
                text = page.text or ""
                if len(text) < min_text_length:
                    continue

                visited_pages.add(title)
                collected += 1
                yield WikiArticle(title=page.title, summary=page.summary, text=text)
