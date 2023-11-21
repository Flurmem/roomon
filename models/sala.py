from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from models.usuario import Usuario

@dataclass
class Sala:
    idSala: int
    idDono: int 
    idCategoria: int
    titulo: str
    descricao: str
    participantes: Optional[List[Usuario]] = ''
    nome: Optional[str] = ""
    nomeUsuario: Optional[str] = ""
    categoria: Optional[str] = ""
    dataCriacao: Optional[datetime] = None
    publica: Optional[bool] = False
    infantil: Optional[bool] = False
