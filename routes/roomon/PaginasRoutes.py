from fastapi import (
    APIRouter,
    Depends,
    Form,
    Path,
    HTTPException,
    Request,
    status,
    Query,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from repositories.categoriaRepo import categoriaRepo
from models.pessoa import Pessoa
from models.categoria import Categoria
from models.sala import Sala
from repositories.pessoaRepo import pessoaRepo
from repositories.salaRepo import salaRepo
from models.usuario import Usuario

from typing import List
from datetime import date

from util.security import (
    obter_hash_senha,
    verificar_senha,
    gerar_token,
    validar_usuario_logado,
)
from util.templateFilters import formatarData, capitalizar_nome_proprio
from util.validators import *
from util.exceptionHandler import *

router = APIRouter()

templates = Jinja2Templates(directory="templates/roomon")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData

# Assinatura Room Plus+ #

@router.get("/assinaturaroomon", response_class=HTMLResponse)
async def getAssineRoomOn(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado)
):
  return templates.TemplateResponse("assinaturaRoomOnConfiguracoes.html", {"request": request, "usuario": usuario})

@router.get("/assinarroomplus", response_class=HTMLResponse)
async def getAssinarRoomPlus(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado),
):
  return templates.TemplateResponse("assinarRoomPlus.html", {"request": request, "usuario": usuario})

@router.get("/assinaturaroomplus", response_class=HTMLResponse)
async def getAssinaturaRoomPlus(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado),
  email: str = Form("")
):
  return templates.TemplateResponse("assinaturaRoomPlusConfiguracoes.html", {"request": request, "usuario": usuario, "email": email})
  
# Suporte # 

@router.get("/perguntasfrequentessuporte", response_class=HTMLResponse)
async def getPerguntasFrequentes(request: Request):
  return templates.TemplateResponse("perguntasFrequentesSuporte.html", {"request": request})

@router.get("/sobrenossuporte", response_class=HTMLResponse)
async def getSobreNos(request: Request):
  return templates.TemplateResponse("sobreNosSuporte.html", {"request": request})

@router.get("/denunciassuporte", response_class=HTMLResponse)
async def getDenuncias(request: Request):
  return templates.TemplateResponse("denunciasSuporte.html", {"request": request})

# Entrando em uma Room #

@router.get("/sala/{nomecriador:str}", response_class=HTMLResponse)
async def getSalaRoomOn(
  request: Request,
  nomecriador: str,
  usuario: Usuario = Depends(validar_usuario_logado),

):
  return templates.TemplateResponse("sala.html", {"request": request, "usuario": usuario})

