from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo para armazenar comandos
class Command(BaseModel):
    source: str  # Origem: "audio" ou "gesture"
    content: str  # Texto do comando ou descrição do gesto
    action: str  # Ação executada

# Lista em memória para registrar comandos
command_history: List[Command] = []

@app.post("/commands/")
def add_command(command: Command):
    """
    Adiciona um comando ao histórico.
    """
    command_history.append(command)
    return {"message": "Comando registrado com sucesso!", "command": command}

@app.get("/commands/")
def get_commands():
    """
    Retorna o histórico de comandos.
    """
    return {"commands": command_history}

@app.get("/")
def root():
    """
    Rota principal para verificar o funcionamento.
    """
    return {"message": "Servidor FastAPI em execução!"}
