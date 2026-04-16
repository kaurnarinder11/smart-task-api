from app.db.database import SessionLocal
from app.models.task import Task


def run_daily_job():
    db = SessionLocal()

    completed = db.query(Task).filter(Task.completed == True).count()
    pending = db.query(Task).filter(Task.completed == False).count()
    

    print("Running daily job...")
    print(f"Completed tasks: {completed}")
    print(f"pending tasks: {pending}")

    if pending > 5:
        print ("Too many pending tasks!")

if __name__ == "__main__" :
    run_daily_job()