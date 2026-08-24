import os
import tempfile
import pandas as pd
import requests
from app.database import SessionLocal, engine
from app.models import Base, Question

# Dataset público con columnas 'question' y 'answer'
DATASET_URL = "https://huggingface.co/datasets/hotpot_qa/resolve/refs%2Fconvert%2Fparquet/distractor/train/0000.parquet"


def download_parquet(url: str) -> str:
    print(f"Descargando {url}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, stream=True)
    r.raise_for_status()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
    tmp.write(r.content)
    tmp.close()
    return tmp.name


def load_questions():
    Base.metadata.create_all(bind=engine)

    parquet_path = download_parquet(DATASET_URL)
    df = pd.read_parquet(parquet_path)
    os.unlink(parquet_path)

    # Tomamos una muestra de 200 filas para no sobrecargar la base de datos
    df = df.head(200)

    print(f"Columnas disponibles: {list(df.columns)}")
    print(f"Filas a insertar: {len(df)}")

    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            question = Question(
                question=str(row.get("question", "")),
                answer=str(row.get("answer", "") or row.get("answer_alias", "")),
                category=str(row.get("type", None)) if "type" in row else None,
                source="HotpotQA",
            )
            session.add(question)

        session.commit()
        print(f"Se insertaron {len(df)} preguntas correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    load_questions()