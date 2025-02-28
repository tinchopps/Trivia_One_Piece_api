import json
from sqlalchemy.orm import Session
from database import SessionLocal, Question

# Cargar preguntas desde el archivo JSON
with open("questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Iniciar sesión con la base de datos
db = SessionLocal()

for item in data["questions"]:
    new_question = Question(
        saga=item["saga"],
        category=item["category"],
        difficulty=item["difficulty"],
        type=item["type"],
        question=item["question"],
        correct_answer=item["correct_answer"],
        incorrect_answers="|".join(item["incorrect_answers"]) if item["type"] == "multiple" else ""
    )
    db.add(new_question)

# Guardar cambios
db.commit()
db.close()

print("✅ Preguntas cargadas correctamente en la base de datos.")
