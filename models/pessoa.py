from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class Pessoa:
    idPessoa: int
    idResponsavel: Optional[int]
    nome: str
    nomeUsuario: str
    email: str
    descricao: Optional[str] = ""
    dataNascimento: Optional[date] = ""
    senha: Optional[str] = ""
    token: Optional[str] = ""
    admin: Optional[bool] = False
    crianca: Optional[bool] = False