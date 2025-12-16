from fastapi import FastAPI
from src.routes.validate_routes import router as validate_router

app = FastAPI(title="SummonMind Validation Service")

app.include_router(validate_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)