"""Seed the database with sample items. Run: python seed.py"""
from datetime import datetime, timedelta

from app.database import Base, SessionLocal, engine
from app.models import Item


SAMPLES = [
    ("Wireless Mouse", "Ergonomic 2.4GHz wireless mouse with USB receiver."),
    ("Mechanical Keyboard", "RGB backlit keyboard with brown switches."),
    ("4K Monitor", "27-inch IPS panel, 60Hz, USB-C."),
    ("Noise-cancelling Headphones", "Over-ear headphones with 30h battery life."),
    ("USB-C Hub", "7-in-1 hub with HDMI, SD, and PD passthrough."),
    ("Webcam 1080p", "Auto-focus webcam with built-in mic."),
    ("Standing Desk Mat", "Anti-fatigue cushioned mat for standing desks."),
    ("Laptop Stand", "Aluminum adjustable laptop riser."),
    ("Desk Lamp", "Dimmable LED lamp with USB charging port."),
    ("Cable Organizer", "Magnetic cable management clips, set of 6."),
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Item).count() > 0:
            print("Items table already populated, skipping.")
            return
        now = datetime.utcnow()
        for i, (name, desc) in enumerate(SAMPLES):
            db.add(Item(name=name, description=desc, created_date=now - timedelta(days=i)))
        db.commit()
        print(f"Inserted {len(SAMPLES)} items.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
