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

    def classify(
        self,
        text: str,
        candidate_labels: list[str],
        label_map: dict[str, str] | None = None,
    ) -> ClassificationResult:
        """
        Clasifica un texto individual contra una lista de categorías candidatas.

        Args:
            text: el texto a clasificar.
            candidate_labels: textos que se le pasan al modelo como opciones
                (recomendado: usar las 'description' de cada categoría, no el
                'name' ni el 'label', para darle al modelo más contexto).
            label_map: diccionario opcional {candidate_label: name_interno}.
                Si se provee, el resultado se traduce de vuelta al 'name'
                corto (ej. "geografia") en vez de dejar la descripción larga
                como category_name / claves de all_scores.
        """
        result = self.pipeline(text, candidate_labels=candidate_labels)

        labels = result["labels"]
        scores = result["scores"]

        if label_map:
            labels = [label_map.get(label, label) for label in labels]

        best_category = labels[0]
        best_score = float(scores[0])
        all_scores = {
            label: float(score)
            for label, score in zip(labels, scores)
        }

        return ClassificationResult(
            category_name=best_category,
            confidence_score=best_score,
            all_scores=all_scores,
        )

    def classify_batch(
        self,
        texts: list[str],
        candidate_labels: list[str],
        label_map: dict[str, str] | None = None,
    ) -> list[ClassificationResult]:
        """
        Clasifica múltiples textos contra las mismas categorías.
        """
        return [
            self.classify(text, candidate_labels, label_map=label_map)
            for text in texts
        ]
    