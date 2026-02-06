from dataclasses import dataclass


@dataclass(frozen=True)
class TrainingConfig:
    language: str = "es"
    root_category: str = "Categoría:Videojuegos"
    max_pages: int = 200
    max_category_depth: int = 2
    min_text_length: int = 400


@dataclass(frozen=True)
class IndexPaths:
    base_dir: str

    @property
    def vectorizer_path(self) -> str:
        return f"{self.base_dir}/vectorizer.pkl"

    @property
    def matrix_path(self) -> str:
        return f"{self.base_dir}/matrix.npz"

    @property
    def metadata_path(self) -> str:
        return f"{self.base_dir}/metadata.json"
