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

# Configurações da conta #

@router.get("/preferenciasconfiguracoes", response_class=HTMLResponse)
async def getPreferenciasConfiguracoes(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado)
):
  return templates.TemplateResponse("preferenciasConfiguracoes.html", {"request": request, "usuario": usuario})

@router.get("/perfilconfiguracoes", response_class=HTMLResponse)
async def getPerfilConfiguracoes(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado)
):
  return templates.TemplateResponse("perfilConfiguracoes.html", {"request": request, "usuario": usuario})

@router.get("/dependentesconfiguracoes", response_class=HTMLResponse)
async def getDependentesConfiguracoes(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado)
):
  return templates.TemplateResponse("dependentesConfiguracoes.html", {"request": request, "usuario": usuario})

  
