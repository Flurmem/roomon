from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Categoria:
    id: int
    nome: str
    descricao: str
    assuntos: str
    infantil: Optional[bool] = False