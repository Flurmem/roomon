from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    admin: Optional[bool] = False
    nomeUsuario: Optional[str] = ''
    descricao: Optional[str] = ""
    idSeguido: Optional[int] = None 
    idSeguidor: Optional[int] = None
    crianca: Optional[bool] = False
    bloqueado: Optional[bool] = False

@dataclass
class Relacao:
    idRelacao: int
    idSeguido: int
    idSeguidor: int
    bloqueado: Optional[bool]
