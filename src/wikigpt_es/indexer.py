import json
from dataclasses import asdict
from typing import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from scipy import sparse

from wikigpt_es.config import IndexPaths
from wikigpt_es.wiki_fetcher import WikiArticle


class WikiIndex:
    def __init__(self, vectorizer: TfidfVectorizer, matrix: sparse.csr_matrix, metadata: list[dict]) -> None:
        self.vectorizer = vectorizer
        self.matrix = matrix
        self.metadata = metadata

    def save(self, paths: IndexPaths) -> None:
        from joblib import dump

        dump(self.vectorizer, paths.vectorizer_path)
        sparse.save_npz(paths.matrix_path, self.matrix)
        with open(paths.metadata_path, "w", encoding="utf-8") as handler:
            json.dump(self.metadata, handler, ensure_ascii=False, indent=2)

    @staticmethod
    def load(paths: IndexPaths) -> "WikiIndex":
        from joblib import load

        vectorizer = load(paths.vectorizer_path)
        matrix = sparse.load_npz(paths.matrix_path)
        with open(paths.metadata_path, "r", encoding="utf-8") as handler:
            metadata = json.load(handler)
        return WikiIndex(vectorizer, matrix, metadata)


def build_index(articles: Iterable[WikiArticle]) -> WikiIndex:
    texts = []
    metadata = []
    for article in articles:
        texts.append(article.text)
        metadata.append(asdict(article))

    vectorizer = TfidfVectorizer(
        strip_accents="unicode",
        lowercase=True,
        max_features=50000,
        ngram_range=(1, 2),
        stop_words=None,
    )
    matrix = vectorizer.fit_transform(texts)
    matrix = normalize(matrix)
    return WikiIndex(vectorizer, matrix, metadata)


def score_query(index: WikiIndex, query: str, top_k: int = 5) -> list[dict]:
    query_vec = index.vectorizer.transform([query])
    query_vec = normalize(query_vec)
    scores = (index.matrix @ query_vec.T).toarray().ravel()
    if scores.size == 0:
        return []
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for idx in top_indices:
        if scores[idx] == 0:
            continue
        entry = dict(index.metadata[idx])
        entry["score"] = float(scores[idx])
        results.append(entry)
    return results
