import datetime
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, APIRouter, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select

# --- 1. DATABASE SETUP (SQLModel) ---
# This represents your "Model Registry" to track model metadata
class ModelRegistry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version: str = Field(index=True)
    date_trained: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    is_active: bool = True

sqlite_url = "sqlite:///./database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# --- 2. VERSIONED ROUTERS (Smooth Rollout) ---

# V1 Router (Legacy/Stable Model)
v1_router = APIRouter(prefix="/v1", tags=["Model v1"])

@v1_router.post("/predict")
async def predict_v1(data: float):
    # Dummy logic: Returns the value as is
    return {"version": "v1", "input": data, "prediction": data * 1.0}

# V2 Router (Improved/Beta Model)
v2_router = APIRouter(prefix="/v2", tags=["Model v2"])

@v2_router.post("/predict")
async def predict_v2(data: float):
    # Dummy logic: Returns double the value to simulate "improvement"
    return {"version": "v2", "input": data, "prediction": data * 2.0}

# --- 3. LIFESPAN EVENT (Startup/Shutdown) ---
# This ensures models are loaded and DB is ready before any request hits
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP LOGIC
    create_db_and_tables()
    
    # Add default "v1" entry to registry if it doesn't exist
    with Session(engine) as session:
        statement = select(ModelRegistry).where(ModelRegistry.version == "v1")
        existing = session.exec(statement).first()
        if not existing:
            default_v1 = ModelRegistry(version="v1", is_active=True)
            session.add(default_v1)
            session.commit()
    
    print("🚀 MLOps Service Started: Model Registry Initialized")
    yield
    # SHUTDOWN LOGIC
    print("🛑 MLOps Service Shutting Down")

# --- 4. MAIN APP CONFIGURATION ---
app = FastAPI(
    title="MLOps Foundations Service",
    description="Simulation for Module 11: Versioned Inference & Model Registry",
    lifespan=lifespan
)

# CRITICAL: Include the versioned routers so they show up in /docs
app.include_router(v1_router)
app.include_router(v2_router)

# --- 5. SYSTEM ENDPOINTS ---

@app.get("/registry", response_model=List[ModelRegistry], tags=["Registry"])
def read_registry(session: Session = Depends(get_session)):
    """Returns a list of all models in the database (Requirement 2)"""
    models = session.exec(select(ModelRegistry)).all()
    return models

@app.get("/health", tags=["System"])
def health_check():
    """Confirms which models are currently served (Production Readiness)"""
    return {
        "status": "online",
        "loaded_models": ["v1", "v2"],
        "environment": "production-simulation"
    }

@app.get("/", include_in_schema=False)
def root():
    return {"message": "MLOps Service is running. Go to /docs for testing."}