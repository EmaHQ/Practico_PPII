"""
Definición centralizada de las categorías disponibles para clasificación.

Cada categoría tiene:
- name: identificador interno (snake_case)
- label: nombre legible para mostrar al usuario
- description: texto que la IA usa para entender el significado de la categoría
"""

CATEGORIES: list[dict[str, str]] = [
    {
        "name": "history",
        "label": "Historia",
        "description": "Preguntas sobre eventos históricos, guerras, tratados, imperios, civilizaciones antiguas y personajes del pasado.",
    },
    {
        "name": "geography",
        "label": "Geografía",
        "description": "Preguntas sobre países, capitales, ciudades, continentes, mapas, océanos, ríos, montañas y fronteras.",
    },
    {
        "name": "science_and_nature",
        "label": "Ciencia y Naturaleza",
        "description": "Preguntas sobre física, química, biología, medicina, astronomía, el universo, plantas, animales y fenómenos naturales.",
    },
    {
        "name": "technology",
        "label": "",
        "description": "Preguntas sobre informática, computadoras, internet, software, hardware, inteligencia artificial y programación.",
    },
    {
        "name": "sports",
        "label": "Deportes",
        "description": "Preguntas sobre disciplinas deportivas, atletas, equipos, torneos, copas mundiales, juegos olímpicos y récords.",
    },
    {
        "name": "entertainment_and_cinema",
        "label": "Cine y Entretenimiento",
        "description": "Preguntas sobre películas, series de televisión, actores, directores de cine, cultura pop y teatro.",
    },
    {
        "name": "music",
        "label": "Música",
        "description": "Preguntas sobre canciones, cantantes, bandas, álbumes musicales, instrumentos, géneros y conciertos.",
    },
    {
        "name": "literature_and_art",
        "label": "Literatura y Arte",
        "description": "Preguntas sobre libros, autores, novelas, poesía, mitología, pintura, escultura, museos y artistas plásticos.",
    },
]


def get_category_names() -> list[str]:
    """Retorna una lista con los nombres (name) de todas las categorías."""
    return [cat["name"] for cat in CATEGORIES]


def get_category_labels() -> list[str]:
    """Retorna una lista con los labels legibles de todas las categorías."""
    return [cat["label"] for cat in CATEGORIES]


def get_category_descriptions() -> list[str]:
    """Retorna una lista con las descripciones de todas las categorías."""
    return [cat["description"] for cat in CATEGORIES]


def find_category_by_name(name: str) -> dict | None:
    """Busca y retorna una categoría por su nombre. Retorna None si no existe."""
    for cat in CATEGORIES:
        if cat["name"] == name:
            return cat
    return None