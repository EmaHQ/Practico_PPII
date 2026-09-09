"""
Módulo de clasificación de texto usando IA.
"""
from dataclasses import dataclass
from transformers import pipeline


@dataclass
class ClassificationResult:
    """
    Resultado de una clasificación.
    """
    category_name: str
    confidence_score: float
    all_scores: dict[str, float]


class AIClassifier:
    """
    Clasificador de texto basado en IA usando zero-shot-classification.
    """

    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        print("Cargando modelo de IA... (puede tardar la primera vez)")
        self.model_name = model_name
        self.pipeline = pipeline("zero-shot-classification", model=model_name)
        print(f"Modelo cargado: {self.model_name}")

    def classify(self, text: str, candidate_labels: list[str]) -> ClassificationResult:
        """
        Clasifica un texto individual contra una lista de categorías candidatas.
        """
        result = self.pipeline(text, candidate_labels=candidate_labels)
        
        best_category = result["labels"][0]
        best_score = float(result["scores"][0])
        all_scores = {
            label: float(score)
            for label, score in zip(result["labels"], result["scores"])
        }

        return ClassificationResult(
            category_name=best_category,
            confidence_score=best_score,
            all_scores=all_scores,
        )

    def classify_batch(self, texts: list[str], candidate_labels: list[str]) -> list[ClassificationResult]:
        """
        Clasifica múltiples textos contra las mismas categorías.
        """
        return [self.classify(text, candidate_labels) for text in texts]