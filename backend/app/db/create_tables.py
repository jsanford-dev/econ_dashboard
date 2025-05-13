from backend.app.db.database import engine
from backend.app.db.models import Base

# Create all tables
Base.metadata.create_all(bind=engine)