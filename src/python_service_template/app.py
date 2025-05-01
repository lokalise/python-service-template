from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from python_service_template.api.coffee import router as countries_router
from python_service_template.api.health import router as health_router


origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app = FastAPI(
    root_path="/api/v1",
    title="Python Service Template",
    description="Batteries-included starter template for Python backend services",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(countries_router)
app.include_router(health_router)
