from fastapi import (
  APIRouter,
  Depends,
  Form,
  Path,
  HTTPException,
  Request,
  status,
  Query,
  File,
  UploadFile,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from io import BytesIO
from repositories.categoriaRepo import categoriaRepo
from models.pessoa import Pessoa
from models.categoria import Categoria
from models.sala import Sala
from repositories.pessoaRepo import pessoaRepo
from repositories.salaRepo import salaRepo
from models.usuario import Usuario
from pydantic import BaseModel

from typing import List
from datetime import date

from util.security import (
  obter_hash_senha,
  verificar_senha,
  gerar_token,
  validar_usuario_logado,
)
from util.templateFilters import formatarData, capitalizar_nome_proprio, formatarIdParaImagem
from util.validators import *
from util.exceptionHandler import *
from util.imageUtil import transformar_em_quadrada
import os
import random

router = APIRouter()

templates = Jinja2Templates(directory="templates/roomon")


@router.on_event("startup")
async def startup_event():
  templates.env.filters["date"] = formatarData
  templates.env.filters["id_img"] = formatarIdParaImagem


# Acessando o perfil do usuário #


@router.get("/perfilusuario", response_class=HTMLResponse)
async def getPerfilUsuario(request: Request,
                           usuario: Usuario = Depends(validar_usuario_logado)):
  if usuario:
    seguidores = int(pessoaRepo.obterQtdeSeguidores(usuario.id))
    seguindo = int(pessoaRepo.obterQtdeSeguindo(usuario.id))
    tem_imagem = False
    if os.path.exists(f"static/images/icone{usuario.id}.jpg"):
      tem_imagem = True
    return templates.TemplateResponse(
      "perfilUsuario0.html", {
        "request": request,
        "usuario": usuario,
        "seguidores": seguidores,
        "seguindo": seguindo,
        "tem_imagem": tem_imagem,
      })

  else:
    return RedirectResponse("/loginroomon")


# Editando o perfil do usuário #


@router.get("/perfilusuarioeditar", response_class=HTMLResponse)
async def getEditarPerfil(request: Request,
                          usuario: Usuario = Depends(validar_usuario_logado)):

  return templates.TemplateResponse("perfilUsuarioEditar.html", {
    "request": request,
    "usuario": usuario
  })


@router.post("/perfilusuarioeditar", response_class=HTMLResponse)
async def postEdicaoPerfilUsuario(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado),
  arquivoImagem: UploadFile = File(...)):

  erros = {}

  conteudo_arquivo = await arquivoImagem.read()
  imagem = Image.open(BytesIO(conteudo_arquivo))
  if not imagem:
    add_error("arquivoImagem", "Nenhuma imagem foi enviada.", erros)

  # se tem erro, mostra o formulário novamente
  if len(erros) > 0:
    valores = {}
    valores["arquivoImagem"] = arquivoImagem
    return templates.TemplateResponse(
      "perfilUsuario0.html",
      {
        "request": request,
        "erros": erros,
        "valores": valores,
      },
    )
  imagem.save(f"static/imagens/perfilRoomOn/icone{usuario.id:04d}.jpg", "JPEG")
  return RedirectResponse("/perfilusuario",
                          status_code=status.HTTP_303_SEE_OTHER)
