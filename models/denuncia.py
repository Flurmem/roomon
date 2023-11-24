from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Denuncia:
    id: int
    idDenunciante: int
    titulo: str
    descricao: str
