from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from database import SessionLocal, Question
from models import Score
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class QuestionCreate(BaseModel):
    saga: str
    category: str
    difficulty: str
    type: str  # "multiple" o "boolean"
    question: str
    correct_answer: str
    incorrect_answers: Optional[List[str]] = []

class AnswerRequest(BaseModel):
    question_id: int
    answer: str
    username: str  # Agregamos el nombre de usuario

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hola, esta es mi API de trivia"}

@app.get("/questions/")
def get_random_questions(
    amount: int = Query(10, gt=0, lt=50),  # Cantidad de preguntas (máx. 50)
    saga: str = None,
    difficulty: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Question)

    if saga:
        query = query.filter(Question.saga == saga)
    
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    questions = query.all()
    random.shuffle(questions)  # Mezclamos preguntas
    questions = questions[:amount]  # Limitamos la cantidad solicitada

    # Mezclar opciones de respuesta
    formatted_questions = []
    for q in questions:
        options = q.incorrect_answers.split("|") + [q.correct_answer]  # Juntar todas las opciones
        random.shuffle(options)  # Mezclar opciones

        formatted_questions.append({
            "id": q.id,
            "saga": q.saga,
            "difficulty": q.difficulty,
            "question": q.question,
            "options": options,  # Opciones mezcladas
            "correct_answer": q.correct_answer
        })

    return {"response_code": 0, "results": formatted_questions}

@app.get("/structured_questions/")
def get_structured_questions(
    saga: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Question)

    if saga:
        query = query.filter(Question.saga == saga)

    # Obtener preguntas por dificultad
    easy_questions = query.filter(Question.difficulty == "easy").all()
    medium_questions = query.filter(Question.difficulty == "medium").all()
    hard_questions = query.filter(Question.difficulty == "hard").all()

    # Mezclar preguntas dentro de cada categoría
    random.shuffle(easy_questions)
    random.shuffle(medium_questions)
    random.shuffle(hard_questions)

    # Seleccionar 4 fáciles, 4 medias y 2 difíciles
    selected_questions = (
        easy_questions[:4] +
        medium_questions[:4] +
        hard_questions[:2]
    )

    # Mezclar respuestas dentro de cada pregunta
    formatted_questions = []
    for q in selected_questions:
        options = q.incorrect_answers.split("|") + [q.correct_answer]
        random.shuffle(options)

        formatted_questions.append({
            "id": q.id,
            "saga": q.saga,
            "difficulty": q.difficulty,
            "question": q.question,
            "options": options,
            "correct_answer": q.correct_answer
        })

    return {"response_code": 0, "results": formatted_questions}

@app.get("/questions/{saga}")
def get_questions_by_saga(saga: str, db: Session = Depends(get_db)):
    return db.query(Question).filter(Question.saga == saga).all()

@app.post("/questions/")
def add_question(question: QuestionCreate, db: Session = Depends(get_db)):
    new_question = Question(
        saga=question.saga,
        category=question.category,
        difficulty=question.difficulty,
        type=question.type,
        question=question.question,
        correct_answer=question.correct_answer,
        incorrect_answers="|".join(question.incorrect_answers) if question.type == "multiple" else ""
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@app.post("/check_answer/")
def check_answer(request: AnswerRequest, db: Session = Depends(get_db)):
    print(f"Received request: {request}")
    question = db.query(Question).filter(Question.id == request.question_id).first()

    if not question:
        print("Pregunta no encontrada")
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    is_correct = question.correct_answer == request.answer
    print(f"Question: {question.question}, Correct Answer: {question.correct_answer}, User Answer: {request.answer}, Is Correct: {is_correct}")

    # Buscar o crear usuario en la tabla de puntuaciones
    user_score = db.query(Score).filter(Score.username == request.username).first()
    
    if not user_score:
        print(f"Usuario {request.username} no encontrado, creando nuevo usuario")
        user_score = Score(username=request.username, points=0)
        db.add(user_score)

    # Sumar puntos si la respuesta es correcta
    if is_correct:
        user_score.points += 10  # Puedes cambiar la cantidad de puntos
        print(f"Respuesta correcta, sumando puntos. Total puntos: {user_score.points}")

    db.commit()

    return {
        "question": question.question,
        "your_answer": request.answer,
        "correct_answer": question.correct_answer,
        "is_correct": is_correct,
        "total_points": user_score.points
    }

@app.get("/score/{username}")
def get_score(username: str, db: Session = Depends(get_db)):
    user_score = db.query(Score).filter(Score.username == username).first()
    
    if not user_score:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"username": username, "points": user_score.points}



