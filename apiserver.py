from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Calculation, Base

app = FastAPI()

# Initialize database
Base.metadata.create_all(bind=engine)

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
def add(num1: int, num2: int, db: Session = Depends(get_db)):
    result = num1 + num2
    calc = Calculation(operation="add", num1=num1, num2=num2, result=result)
    db.add(calc)
    db.commit()
    return {"result": result}

@app.get("/subtract/{num1}/{num2}")
def subtract(num1: int, num2: int, db: Session = Depends(get_db)):
    result = num1 - num2
    calc = Calculation(operation="subtract", num1=num1, num2=num2, result=result)
    db.add(calc)
    db.commit()
    return {"result": result}

@app.get("/multiply/{num1}/{num2}")
def multiply(num1: int, num2: int, db: Session = Depends(get_db)):
    result = num1 * num2
    calc = Calculation(operation="multiply", num1=num1, num2=num2, result=result)
    db.add(calc)
    db.commit()
    return {"result": result}

@app.get("/calculations")
def get_calculations(db: Session = Depends(get_db)):
    calculations = db.query(Calculation).all()
    return calculations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apiserver:app", host="127.0.0.1", port=8000, reload=True)
