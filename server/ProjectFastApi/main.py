from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database.connection import init_db
from routes import auth, service, components, stuff
from utils.auth import get_current_user

app = FastAPI(title="Computer Service API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(service.router, prefix="/service", tags=["Service"])
app.include_router(components.router, prefix="/components", tags=["Components"])
app.include_router(stuff.router, prefix="/stuff", tags=["Stuff"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Computer Service API"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
