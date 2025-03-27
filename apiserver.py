from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Calculation

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Calculator API with Database!"}

@app.get("/add/{num1}/{num2}")
def add(num1: int, num2: int):
    return {"result": num1 + num2}

@app.get("/subtract/{num1}/{num2}")
def subtract(num1: int, num2: int):
    return {"result": num1 - num2}

@app.get("/multiply/{num1}/{num2}")
def multiply(num1: int, num2: int):
    return {"result": num1 * num2}

# Save calculation to database
@app.get("/save/{operation}/{num1}/{num2}/{result}")
def save_result(operation: str, num1: int, num2: int, result: int, db: Session = Depends(get_db)):
    calculation = Calculation(operation=operation, num1=num1, num2=num2, result=result)
    db.add(calculation)
    db.commit()
    return {"message": "Calculation saved to database!"}

# Retrieve all calculations
@app.get("/calculations")
def get_calculations(db: Session = Depends(get_db)):
    return db.query(Calculation).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apiserver:app", host="127.0.0.1", port=8000, reload=True)
