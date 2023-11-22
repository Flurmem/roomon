from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Denuncia:
    id: int
    idDenunciante: str
    titulo: str
    descricao: str