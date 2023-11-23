from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from repositories.categoriaRepo import categoriaRepo
from models.pessoa import Pessoa
from models.categoria import Categoria
from models.usuario import Usuario
from repositories.denunciaRepo import denunciaRepo
from repositories.pessoaRepo import pessoaRepo
from util.templateFilters import formatarData
from typing import List

from util.security import *
from util.templateFilters import *
from util.validators import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem

@router.get("/criarcategoria", response_class=HTMLResponse)
async def getCriarCategoria(request: Request,
                          usuario: Usuario = Depends(validar_usuario_logado),
                          crianca: Usuario = Depends(validar_crianca_logado)
                          ):

  if usuario:
    return templates.TemplateResponse(
      "kids/administracao/categoriaAdm.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.get("/dashboard", response_class=HTMLResponse)
async def getDashboard(request: Request,
                          usuario: Usuario = Depends(validar_usuario_logado),
                          crianca: Usuario = Depends(validar_crianca_logado)
                          ):

  if usuario:
    return templates.TemplateResponse(
      "kids/administracao/dashboardAdm.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.get("/denunciasadm", response_class=HTMLResponse)
async def getDenunciasAdm(request: Request,
                          usuario: Usuario = Depends(validar_usuario_logado),
                          crianca: Usuario = Depends(validar_crianca_logado)
                          ):

  if usuario:
    denunciasTotais = denunciaRepo.obterDenunciasTotais()
    return templates.TemplateResponse(
      "kids/administracao/denunciaAdm.html", {"request": request, "usuario": usuario, "crianca": crianca, "denunciasTotais":denunciasTotais})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.get("/adm", response_class=HTMLResponse)
async def getAdm(request: Request,
                          usuario: Usuario = Depends(validar_usuario_logado),
                          crianca: Usuario = Depends(validar_crianca_logado)
                          ):

  if usuario:
    return templates.TemplateResponse(
      "kids/administracao/inicialAdm.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)
