from fastapi import APIRouter, Depends, File, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from repositories.categoriaRepo import categoriaRepo
from models.websocket import ConnectionManager
from models.usuario import Usuario
from repositories.pessoaRepo import pessoaRepo

from util.security import (
    validar_usuario_logado,
    validar_crianca_logado,
)
from util.templateFilters import *
from util.validators import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")

manager = ConnectionManager()

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem

@router.get("/inicialresponsavel", response_class=HTMLResponse)
async def getEsqueceuSenha(request: Request,
                          usuario: Usuario = Depends(validar_usuario_logado),
                          crianca: Usuario = Depends(validar_crianca_logado)
                          ):

  if usuario:
    return templates.TemplateResponse(
      "kids/responsavel/inicialResponsavel.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)


@router.get("/perfilresponsavel", response_class=HTMLResponse)
async def getEsqueceuSenha(request: Request,
                          usuario: Usuario = Depends(validar_usuario_logado),
                          crianca: Usuario = Depends(validar_crianca_logado)
                          ):

  if usuario:
    dependentes = pessoaRepo.obterDependentes(usuario.id)
    return templates.TemplateResponse(
      "kids/responsavel/perfilResponsavel.html", {"request": request, "usuario": usuario, "crianca": crianca, "dependentes": dependentes})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)


@router.get("/assinar", response_class=HTMLResponse)
async def getDenuncias(request: Request,
                       usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):
  if usuario:
    return templates.TemplateResponse(
      "kids/responsavel/assinarRoomplus.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)


@router.get("/editarperfil", response_class=HTMLResponse)
async def getEditarPerfil(request: Request,usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):
  if usuario:
    return templates.TemplateResponse(
      "kids/responsavel/preferenciasConfiguracoes.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)


 # CONFIGURAÇÕES

@router.get("/configuracoes", response_class=HTMLResponse)
async def getConfiguracoes(request: Request,usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):
  if usuario:
    return templates.TemplateResponse(
      "kids/responsavel/configuracoesResponsavel.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.get("/preferencias", response_class=HTMLResponse)
async def getDenuncias(request: Request,usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):
  if usuario:
    return templates.TemplateResponse(
      "kids/responsavel/preferenciasConfiguracoes.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.get("/assinatura", response_class=HTMLResponse)
async def getDenuncias(request: Request,
                       usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):
  if usuario:
    return templates.TemplateResponse(
      "kids/responsavel/assinaturaRoomOnConfiguracoes.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.get("/dependentes", response_class=HTMLResponse)
async def getDenuncias(request: Request,
                       usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):
  if usuario:
    return templates.TemplateResponse(
      "kids/responsavel/dependentesConfiguracoes.html", {"request": request, "usuario": usuario, "crianca": crianca})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)
