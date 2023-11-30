from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Chat:
    idChat: int
    idSala: int
    dataCriacao: Optional[datetime] = None

@dataclass
class Mensagem:
    idMensagem: int
    idChat: int
    idEmissor: int
    conteudo: str
    dataEnvio: Optional[datetime] = None
    nomeUsuario: Optional[str] = ''

