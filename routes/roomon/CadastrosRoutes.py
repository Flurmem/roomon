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


# Cadastro Usuário Room ON #

@router.get("/cadastroroomon", response_class=HTMLResponse)
async def getCadastroRoomOn(
  request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
  return templates.TemplateResponse("cadastroRoomOn.html", {
    "request": request,
    "usuario": usuario,
  },
)

@router.post("/cadastroroomon", response_class=HTMLResponse)
async def postCadastroRoomOn(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado),
  nome: str = Form(""),
  nomeUsuario: str = Form(""),
  email: str = Form(""),
  dataNascimento: date = Form(""),
  senha: str = Form(""),
  cSenha: str = Form(""),
  returnUrl: str = Query("/perfilusuario")
):
  nome = capitalizar_nome_proprio(nome).strip()
  email = email.lower().strip()
  senha = senha.strip()
  cSenha = cSenha.strip()

  erros = {}
    # validação do campo nome
  is_not_empty(nome, "nome", erros)
  is_person_fullname(nome, "nome", erros)
  is_not_empty(nomeUsuario, "nomeUsuario", erros)
  is_not_empty(email, "email", erros)
  is_not_empty(dataNascimento, "dataNascimento", erros)
  is_not_empty(senha, "senha", erros)
  is_password(senha, "senha", erros)
  is_not_empty(cSenha, "cSenha", erros)
  is_matching_fields(cSenha, "cSenha", senha, "senha", erros)
  
  if is_email(email, "email", erros):
    if pessoaRepo.emailExiste(email):
      add_error("email", "Já existe um usuário cadastrado com este e-mail.", erros)

  # validação da imagem
  


  if len(erros) > 0:
    valores = {}
    valores["nome"] = nome
    valores["email"] = email.lower()
    valores['dataNascimento'] = str(dataNascimento)
    valores["nomeUsuario"] = nomeUsuario
    

    return templates.TemplateResponse(
      "cadastroRoomOn.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )
  
  usuarioCadastro = pessoaRepo.cadastro(
      Pessoa(
        idPessoa = 0,
        idResponsavel=None,
        nome = nome,
        nomeUsuario = nomeUsuario,
        email = email,
        dataNascimento = dataNascimento,
        senha = obter_hash_senha(senha),
      )
  )

  if (usuarioCadastro):
    
    return RedirectResponse(
        "/perfilusuario", status_code=status.HTTP_303_SEE_OTHER
    )
  
  token = gerar_token()
  
  if pessoaRepo.alterarToken(email, token):
    response = RedirectResponse(returnUrl, status.HTTP_302_FOUND)
    response.set_cookie(
      key = "auth_token", value = token, max_age = 1800, httponly=True
    )
    return response
  else:
    raise Exception(
      "Não foi possível alterar o token do usuário no banco de dados."
    )



# Cadastrando uma Room no sistema #

@router.get("/criacaosala", response_class=HTMLResponse)
async def getCriacaoSala(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado)
):
  if usuario:
    categorias = categoriaRepo.lerTodos()
    return templates.TemplateResponse("criacaoSala.html", {"request": request, "usuario": usuario, "categorias": categorias,})
  else:
    return RedirectResponse("/loginroomon", status.HTTP_302_FOUND)
    
@router.post("/criacaosala")
async def postCriacaoRoom(
  request: Request,
  usuario: Usuario = Depends(validar_usuario_logado),
  titulo: str = Form(...),
  categoria: int = Form(...),
  descricao: str = Form(...),
  publica: bool = Form(...),
  arquivoImagem: UploadFile = File(...),
):
  if usuario:
    categorias = categoriaRepo.lerTodos()
    erros = {}
    
    is_not_empty(titulo, "titulo", erros)
    is_not_empty(categoria, "categorias", erros)
    is_not_empty(descricao, "descricao", erros)

    conteudo_arquivo = await arquivoImagem.read()
    imagem = Image.open(BytesIO(conteudo_arquivo))
    if not imagem:
      add_error("arquivoImagem", "Nenhuma imagem foi enviada.", erros)

    if len(erros) > 0:
      valores = {}
      valores["titulo"] = titulo
      return templates.TemplateResponse(
        "criacaoSala.html",
        {
          "request": request,
          "erros": erros,
          "valores": valores,
          "categorias": categorias,
        }
      )

    sala = salaRepo.insert(
      Sala(
        idSala = 0,
        idDono = usuario.id,
        idCategoria = categoria,
        titulo = titulo,
        descricao = descricao,
        publica = publica,
      )
    )

    if sala:      
      imagem.save(f"static/imagens/salasRoomOn/capa{sala.idSala:04d}.jpg", "JPEG")
      # return RedirectResponse("/sala/{usuario.nomeUsuario}")
    return RedirectResponse("/inicio", status.HTTP_302_FOUND)
  else:
    return RedirectResponse("/loginroomon", status.HTTP_302_FOUND)