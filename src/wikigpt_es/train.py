import argparse
import os

from wikigpt_es.config import IndexPaths, TrainingConfig
from wikigpt_es.indexer import build_index
from wikigpt_es.wiki_fetcher import WikipediaVideoGameFetcher


def train_model(output_dir: str, config: TrainingConfig) -> None:
    os.makedirs(output_dir, exist_ok=True)
    fetcher = WikipediaVideoGameFetcher(config.language)

    articles = list(
        fetcher.iter_video_game_articles(
            root_category=config.root_category,
            max_pages=config.max_pages,
            max_depth=config.max_category_depth,
            min_text_length=config.min_text_length,
        )
    )
    if not articles:
        raise RuntimeError("No se encontraron artículos para entrenar el índice.")

    index = build_index(articles)
    index.save(IndexPaths(output_dir))


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrena el índice WikiGPT-ES desde cero.")
    parser.add_argument("--output", default="data", help="Directorio de salida del índice.")
    parser.add_argument("--max-pages", type=int, default=200, help="Máximo de artículos a descargar.")
    parser.add_argument("--max-depth", type=int, default=2, help="Profundidad de categorías.")
    args = parser.parse_args()

    config = TrainingConfig(max_pages=args.max_pages, max_category_depth=args.max_depth)
    train_model(args.output, config)


if __name__ == "__main__":
    main()
