from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from app.models import User, PredictionLog, PredictionRequest
from app.auth import hash_password, verify_password, create_access_token, get_current_user_username
from app.inference import model_registry, load_weights, perform_inference
import json

# -----------------------------
# Database Setup
# -----------------------------
sqlite_url = "sqlite:///./production_ai.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

# -----------------------------
# Lifespan Management
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB and Load Models
    SQLModel.metadata.create_all(engine)
    model_registry["active_model"] = load_weights("churn_classifier")
    print("AI Model Ready for Production Traffic")
    yield
    # Shutdown: Cleanup (optional)
    model_registry.clear()

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="Capstone Production AI Service", lifespan=lifespan)

@app.post("/signup")
def signup(username: str, password: str, session: Session = Depends(get_session)):
    # Check if user exists
    statement = select(User).where(User.username == username)
    if session.exec(statement).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create user
    new_user = User(username=username, hashed_password=hash_password(password))
    session.add(new_user)
    session.commit()
    return {"msg": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/predict")
def predict(
    request: PredictionRequest, 
    username: str = Depends(get_current_user_username), 
    session: Session = Depends(get_session)
):
    # 1. Fetch User
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    
    # 2. Perform Inference
    prediction_result = perform_inference(request.feature_vector)
    
    # 3. Log to DB (Auditing)
    new_log = PredictionLog(
        user_id=user.id,
        input_data=json.dumps(request.feature_vector),
        prediction=prediction_result
    )
    session.add(new_log)
    session.commit()
    
    return {
        "user": username,
        "prediction": prediction_result,
        "model_version": model_registry["active_model"]
    }
