"""
Script principal de categorización.
"""
from tqdm import tqdm
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Question, Categorization
from app.categories import CATEGORIES, get_category_names, get_category_labels_en
from app.classifier import AIClassifier
from app.human_review import (
    display_question_context,
    confirm_ai_suggestion,
    ask_human_for_category,
)

CONFIDENCE_THRESHOLD = 0.30


def get_uncategorized_questions(db) -> list:
    subquery = select(Categorization.question_id)
    return db.query(Question).filter(~Question.id.in_(subquery)).all()


def save_categorization(
    db,
    question_id: int,
    category_name: str,
    confidence_score: float,
    is_automatic: bool,
) -> None:
    try:
        categorization = Categorization(
            question_id=question_id,
            category_name=category_name,
            confidence_score=confidence_score,
            is_automatic=is_automatic,
        )
        db.add(categorization)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error al guardar categorización: {e}")


def categorize_all(batch_size: int = 32, threshold: float = CONFIDENCE_THRESHOLD) -> None:
    db = SessionLocal()

    try:
        classifier = AIClassifier()
        category_names = get_category_names()
        category_labels_en = get_category_labels_en()

        # Le pasamos al modelo etiquetas cortas EN INGLÉS (ej. "geography",
        # "science and technology"), no la descripción completa: el pipeline
        # arma la hipótesis "This example is about {label}." y necesita una
        # palabra/frase corta y coherente ahí, no un párrafo entero.
        # Después traducimos el resultado de vuelta al "name" interno en
        # español (ej. "geografia") con este mapeo.
        label_en_to_name = dict(zip(category_labels_en, category_names))

        questions = get_uncategorized_questions(db)

        print("\n" + "=" * 50)
        print("  Categorizador de Preguntas con IA")
        print("=" * 50)
        print(f"  Preguntas pendientes: {len(questions)}")
        print(f"  Categorías: {len(category_names)}")
        print(f"  Umbral de confianza: {int(threshold * 100)}%")
        print("=" * 50 + "\n")

        if not questions:
            print("No hay preguntas pendientes de categorización.")
            return

        auto_count = 0
        manual_count = 0
        skipped_count = 0

        for q in tqdm(questions, desc="Categorizando"):
            result = classifier.classify(
                q.question,
                category_labels_en,
                label_map=label_en_to_name,
            )

            if result.confidence_score >= threshold:
                save_categorization(
                    db=db,
                    question_id=q.id,
                    category_name=result.category_name,
                    confidence_score=result.confidence_score,
                    is_automatic=True,
                )
                auto_count += 1
            else:
                display_question_context(
                    question_text=q.question,
                    ai_suggestion=result.category_name,
                    confidence=result.confidence_score,
                    all_scores=result.all_scores,
                )

                if confirm_ai_suggestion(result.category_name, result.confidence_score):
                    save_categorization(
                        db=db,
                        question_id=q.id,
                        category_name=result.category_name,
                        confidence_score=result.confidence_score,
                        is_automatic=False,
                    )
                    manual_count += 1
                else:
                    chosen = ask_human_for_category(CATEGORIES)
                    if chosen:
                        save_categorization(
                            db=db,
                            question_id=q.id,
                            category_name=chosen,
                            confidence_score=1.0,
                            is_automatic=False,
                        )
                        manual_count += 1
                    else:
                        skipped_count += 1

        print("\n" + "=" * 50)
        print("  Resumen de categorización")
        print("=" * 50)
        print(f"  Total procesadas: {auto_count + manual_count + skipped_count}")
        print(f"  Automáticas: {auto_count}")
        print(f"  Manuales: {manual_count}")
        print(f"  Omitidas: {skipped_count}")
        print("=" * 50 + "\n")

    finally:
        db.close()


if __name__ == "__main__":
    categorize_all()
