"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, usuarios, conversas, documentos, avaliacoes, admin

app = FastAPI(
    title="Chatbot IFES API",
    description="API para o sistema de chatbot de consulta a documentos do IFES",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(conversas.router)
app.include_router(documentos.router)
app.include_router(avaliacoes.router)
app.include_router(admin.router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Chatbot IFES API está no ar"}
