from typing import Optional
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Base, Question

app = FastAPI(title="Questions API", version="1.0.0")


# Esquema Pydantic para validar los datos recibidos en el POST
class QuestionCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    source: Optional[str] = None


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Questions API funcionando",
        "endpoints": [
            "/questions",
            "/questions/{id}",
            "/questions/category/{category}",
            "/stats",
        ],
    }


# Punto 2: Estadísticas globales y por categoría
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Question).count()

    counts_by_category = (
        db.query(Question.category, func.count(Question.id))
        .group_by(Question.category)
        .all()
    )

    cat_summary = {
        (cat if cat else "Sin categoría"): count for cat, count in counts_by_category
    }

    return {"total_questions": total, "by_category": cat_summary}


# Punto 1: Filtrar preguntas por categoría
@app.get("/questions/category/{category}")
def get_questions_by_category(category: str, db: Session = Depends(get_db)):
    return db.query(Question).filter(Question.category == category).all()


@app.get("/questions")
def list_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    questions = db.query(Question).offset(skip).limit(limit).all()
    return questions


@app.get("/questions/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return {"error": "Pregunta no encontrada"}
    return question


# Punto 4: Crear una nueva pregunta vía POST
@app.post("/questions", status_code=status.HTTP_201_CREATED)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    new_question = Question(
        question=payload.question,
        answer=payload.answer,
        category=payload.category,
        source=payload.source or "Manual",
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@app.get("/questions/category/{category_name}")
def list_by_category(category_name: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna las preguntas que fueron categorizadas con una categoría específica.

    TAREA:
    - Hacer un JOIN entre Question y Categorization
    - Filtrar por Categorization.category_name == category_name
    - Aplicar skip y limit
    - Retornar las preguntas con su información de categorización

    TODO: Implementar la query con JOIN.
    """
    # TODO: Implementar
    pass


@app.get("/categories")
def list_categories():
    """
    Retorna la lista de categorías disponibles.

    TAREA:
    - Importar CATEGORIES desde app/categories.py
    - Retornar la lista completa

    TODO: Implementar.
    """
    # TODO: Implementar
    pass


@app.get("/categories/stats")
def category_stats(db: Session = Depends(get_db)):
    """
    Retorna estadísticas de categorización.

    Debe retornar un JSON como:
    {
        "total_questions": 1000,
        "categorized": 850,
        "uncategorized": 150,
        "automatic": 700,
        "manual": 150,
        "by_category": {
            "machine_learning": 200,
            "historia": 150,
            ...
        }
    }

    TAREA:
    - Contar el total de preguntas
    - Contar las categorizadas (que tienen entrada en categorizations)
    - Contar automáticas vs manuales
    - Agrupar por categoría (GROUP BY)

    TODO: Implementar las queries necesarias.
    Pista: usá db.query(func.count(...)).group_by(...)
    """
    # TODO: Implementar
    pass