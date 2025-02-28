# One Piece Trivia API

Una API de trivia basada en el mundo de *One Piece*, con preguntas organizadas por sagas y diferentes niveles de dificultad.

## 🚀 Instalación y Ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/tu_repo.git
cd tu_repo
```

### 2️⃣ Crear un entorno virtual e instalar dependencias
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Ejecutar la API
```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`

## 📌 Endpoints

### 🔹 Obtener preguntas aleatorias
```http
GET /questions?amount=10
```
**Parámetros opcionales:**
- `amount` (int): Número de preguntas a obtener (por defecto 10)
- `difficulty` (string): Nivel de dificultad (`easy`, `medium`, `hard`)
- `saga` (string): Filtrar por saga específica

**Ejemplo de respuesta:**
```json
{
  "response_code": 0,
  "results": [
    {
      "type": "multiple",
      "difficulty": "easy",
      "saga": "East Blue",
      "question": "¿Cómo se llama el primer barco de Luffy?",
      "correct_answer": "Going Merry",
      "incorrect_answers": [
        "Thousand Sunny",
        "Red Force",
        "Moby Dick"
      ]
    }
  ]
}
```

### 🔹 Documentación automática (Swagger)
Una vez que la API está corriendo, podés ver la documentación en:
- `http://127.0.0.1:8000/docs` (Swagger UI)
- `http://127.0.0.1:8000/redoc` (ReDoc)

---

## 🛠 Tecnologías
- **Python** (FastAPI)
- **Uvicorn** (Servidor ASGI)
- **SQLite/PostgreSQL** (Base de datos)

## 📌 Autor
**[Tinchopps]** - Creado con amor por *One Piece* 🏴‍☠️
