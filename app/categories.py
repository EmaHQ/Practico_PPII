"""
Definición centralizada de las categorías disponibles para clasificación.

Cada categoría tiene:
- name: identificador interno (snake_case), usado en BD y URLs.
- label: nombre legible en español, para mostrar al usuario (consola, API).
- label_en: palabra/frase corta en inglés, usada como candidate_label del
  modelo de IA. Las preguntas del dataset están en inglés, así que el
  candidate_label debe estar en el mismo idioma para que el pipeline de
  zero-shot arme una hipótesis coherente ("This example is about {label_en}.").
- description: descripción detallada en inglés, solo como referencia humana
  (documentación). No se le pasa al modelo tal cual porque el pipeline
  espera una palabra/frase corta, no un párrafo, en el lugar de "{}".
"""

CATEGORIES: list[dict[str, str]] = [
    {
        "name": "geografia",
        "label": "Geografía",
        "label_en": "geography",
        "description": "Questions about countries, capitals, cities, continents, maps, oceans, rivers, mountains, borders, and geographic locations.",
    },
    {
        "name": "ciencia",
        "label": "Ciencia",
        "label_en": "science and technology",
        "description": "Questions about physics, chemistry, biology, medicine, astronomy, mathematics, technology, the universe, plants, animals, and natural phenomena.",
    },
    {
        "name": "historia",
        "label": "Historia",
        "label_en": "history",
        "description": "Questions about historical events, wars, treaties, empires, ancient civilizations, revolutions, and figures from the past.",
    },
    {
        "name": "deporte",
        "label": "Deporte",
        "label_en": "sports",
        "description": "Questions about sports disciplines, athletes, teams, tournaments, world cups, olympic games, and sports records.",
    },
    {
        "name": "arte",
        "label": "Arte",
        "label_en": "art and literature",
        "description": "Questions about painting, sculpture, literature, poetry, museums, visual artists, architecture, and mythology.",
    },
    {
        "name": "entretenimiento",
        "label": "Entretenimiento",
        "label_en": "entertainment",
        "description": "Questions about movies, TV series, actors, film directors, music, singers, bands, pop culture, and theater.",
    },
]


def get_category_names() -> list[str]:
    """Retorna una lista con los nombres (name) de todas las categorías."""
    return [cat["name"] for cat in CATEGORIES]


def get_category_labels() -> list[str]:
    """Retorna una lista con los labels legibles (español) de todas las categorías."""
    return [cat["label"] for cat in CATEGORIES]


def get_category_labels_en() -> list[str]:
    """Retorna una lista con los labels cortos en inglés, para pasarle al modelo de IA."""
    return [cat["label_en"] for cat in CATEGORIES]


def get_category_descriptions() -> list[str]:
    """Retorna una lista con las descripciones de todas las categorías."""
    return [cat["description"] for cat in CATEGORIES]


def find_category_by_name(name: str) -> dict | None:
    """Busca y retorna una categoría por su nombre. Retorna None si no existe."""
    for cat in CATEGORIES:
        if cat["name"] == name:
            return cat
    return None