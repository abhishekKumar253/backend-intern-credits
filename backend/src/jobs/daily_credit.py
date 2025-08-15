from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime,timezone
from src.database.connection import SessionLocal
from src.models.credits import Credit

def add_daily_credits():
    db: Session = SessionLocal()
    try:
        users_credits = db.query(Credit).all()
        for credit in users_credits:
            credit.credits += 5
            credit.last_updated = datetime.now(timezone.utc)
        db.commit()
        print(f"[{datetime.now(timezone.utc)}] Added 5 daily credits to all users.")
    except Exception as e:
        print(f"Error in daily credit job: {e}")
        db.rollback()
    finally:
        db.close()

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(add_daily_credits, 'cron', hour=0, minute=0)
scheduler.start()

print("Daily credit scheduler started.")