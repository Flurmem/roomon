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
from util.imageUtil import transformar_em_quadrada
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

router = APIRouter()

templates = Jinja2Templates(directory="templates/roomon")

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem


@router.get("/inicio", response_class=HTMLResponse)
async def getPaginaInicial(
  request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
  if usuario:
    salas = salaRepo.obterSalas()
    categorias = categoriaRepo.lerTodos()
    return templates.TemplateResponse("logadoRoomOn.html", {"request": request, "salas": salas, "categorias": categorias}
    )
  else:
    return RedirectResponse("/loginroomon", status.HTTP_302_FOUND)

@router.get("/loginroomon",response_class=HTMLResponse)
async def getLoginRoomOn(
  request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
  return templates.TemplateResponse("/loginRoomOn.html", {"request": request, "usuario": usuario}
  )

@router.post("/loginroomon")
async def postLoginRoomOn(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado),
  email: str = Form(""),
  senha: str = Form(""),
  returnUrl: str = Query("/inicio")
):
  email = email.strip().lower()
  senha = senha.strip()

  erros = {}

  is_not_empty(email, "email", erros)
  is_email(email, "email", erros)
  is_not_empty(senha, "senha", erros)

  if len(erros) == 0:
    hash_senha_bd = pessoaRepo.obterSenhaDeEmail(email)
    if hash_senha_bd:
      boolSenha = verificar_senha(senha, hash_senha_bd)
      if verificar_senha(senha, hash_senha_bd):
        token = gerar_token()
        if pessoaRepo.alterarToken(email, token):
          response = RedirectResponse(returnUrl, status.HTTP_302_FOUND)
          response.set_cookie(
          key="auth_token", value=token, max_age=1800, httponly=True)
          return response
        else:
          raise Exception("Não foi possível alterar o token do usuário no banco de dados.")
      else:
        add_error("senha", "Senha não confere.", erros)
    else:
      add_error("email", "Usuário não cadastrado.", erros)

  if len(erros) > 0:
        valores = {}
        valores["email"] = email
        return templates.TemplateResponse(
            "loginRoomOn.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )

@router.get("/esqueceusenha", response_class=HTMLResponse)
async def getEsqueceuSenha(request: Request):
  return templates.TemplateResponse("esqueceuSenhaRoomOn.html", {"request": request})

@router.post("/esqueceusenha", response_class=HTMLResponse)
async def postEsqueceuSenha(
  request: Request,
  email: str = Form(""),
):
  return templates.TemplateResponse("esqueceuSenhaRoomOn.html", {"request": request, "email": email})

@router.get("/logoutroomon")
async def getLogoutRoomOn(request: Request):
  response = RedirectResponse("/", status.HTTP_302_FOUND)
  response.set_cookie(key="auth_token", value="", httponly=True, expires="1970-01-01T00:00:00Z")
  return response





