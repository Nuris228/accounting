from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from . import models, database
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from . import models, database

app = FastAPI()

# Зависимость для получения сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transactions/")
def create_transaction(transaction: models.Transaction, db: Session = Depends(get_db)):
    db_transaction = database.DBTransaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(database.DBTransaction).all()

@app.get("/transactions/{type}/")  # /transactions/income/ или /transactions/expense/
def get_transactions_by_type(type: str, db: Session = Depends(get_db)):
    if type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Неправильный тип операции")
    return db.query(database.DBTransaction).filter(database.DBTransaction.type == type).all()


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')



# See PyCharm help at https://www.jetbrains.com/help/pycharm/


