"""
Módulo de revisión humana por consola.

Cuando la IA no tiene suficiente confianza (score < threshold),
este módulo le pregunta al usuario por terminal qué categoría corresponde.
"""


def display_question_context(
    question_text: str,
    ai_suggestion: str,
    confidence: float,
    all_scores: dict[str, float],
) -> None:
    """
    Muestra al usuario la pregunta, la sugerencia de la IA y los scores.
    """
    print("\n" + "═" * 64)
    print(" REVISIÓN MANUAL REQUERIDA (confianza < 70%)")
    print("═" * 64)
    print(f"\nPregunta: {question_text}\n")
    print(f"Sugerencia de la IA: {ai_suggestion} (confianza: {confidence * 100:.1f}%)\n")
    print("Scores de todas las categorías:")

    # Ordenar scores de mayor a menor
    sorted_scores = sorted(all_scores.items(), key=lambda item: item[1], reverse=True)
    for idx, (cat, score) in enumerate(sorted_scores, start=1):
        print(f"  {idx:2d}. {cat:<26} → {score * 100:.1f}%")

    print("═" * 64)


def ask_human_for_category(categories: list[dict[str, str]]) -> str | None:
    """
    Le pide al usuario que elija una categoría por consola.
    """
    print("\nOpciones:")
    for idx, cat in enumerate(categories, start=1):
        label = cat.get("label", cat.get("name", "Desconocida"))
        print(f"  {idx:2d}. {label}")
    print("   S. Skip (omitir esta pregunta)\n")

    while True:
        choice = input("Elegí una opción: ").strip()
        if choice.lower() == "s":
            return None
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(categories):
                return categories[num - 1]["name"]
        print(f"Opción inválida. Ingresá un número de 1 a {len(categories)} o 'S' para omitir.")


def confirm_ai_suggestion(ai_suggestion: str, confidence: float) -> bool:
    """
    Pregunta al usuario si acepta la sugerencia de la IA.
    """
    conf_pct = int(confidence * 100) if confidence <= 1.0 else int(confidence)
    choice = input(f'\n¿Aceptás la sugerencia "{ai_suggestion}" ({conf_pct}%)? [S/n]: ').strip().lower()
    return choice in ("", "s", "si", "sí", "y", "yes")