# routes/ProjetoRoutes.py
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
from repositories.pessoaRepo import pessoaRepo
from repositories.salaRepo import salaRepo
from models.usuario import Usuario

from typing import List
from datetime import date

from util.security import *
from util.templateFilters import *
from util.validators import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem



@router.get("/cadastro", response_class=HTMLResponse)
# address of the route and type of return
async def getCadastroAdulto(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    categorias = categoriaRepo.lerTodos()
    return templates.TemplateResponse(
        "kids/cadastro/cadastro.html",
        {
            "request": request,
            "categorias": categorias,
            "categoriasCount": len(categorias),
            "usuario": usuario,
        },
    )


@router.post("/cadastro", response_class=HTMLResponse)
async def postCadastro(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    nome: str = Form(""),
    nomeUsuario: str = Form(""),
    email: str = Form(""),
    dataNascimento: date = Form(""),
    crianca: bool = True,
    categorias: List[int] = Form(""),
    returnUrl: str = Query("/inicialkids"),
):
      nome = capitalizar_nome_proprio(nome).strip()
      email = email.lower().strip()

      erros = {}

      is_not_empty(nome, "nome", erros)
      is_person_fullname(nome, "nome", erros)
      # validação do campo email
      is_not_empty(email, "email", erros)
      if is_email(email, "email", erros):
          if pessoaRepo.emailExiste(email):
              add_error("email", "Já existe um usuário cadastrado com este e-mail.", erros)
      # validação do campo senha
  
      is_not_empty(nomeUsuario, "nomeUsuario", erros)
  
      is_not_empty(dataNascimento, "dataNascimento", erros)
  
      categoriasLista = categoriaRepo.lerTodos()
      # se tem erro, mostra o formulário novamente
      if len(erros) > 0:
          valores = {}
          valores["nome"] = nome
          valores["email"] = email.lower()
          valores['dataNascimento'] = str(dataNascimento)
          valores["nomeUsuario"] = nomeUsuario
  
          return templates.TemplateResponse(
              "kids/cadastro/cadastro.html",
              {
                  "request": request,
                  "usuario": usuario,
                  "erros": erros,
                  "valores": valores,
                  "categorias": categoriasLista,
                  "categoriasCount": len(categorias),
              },
          )
  
  
      usuarioCadastro = Pessoa(
          idPessoa=0,
          idResponsavel=usuario.id,
          nome=nome,
          nomeUsuario=nomeUsuario,
          email=email,
          dataNascimento=dataNascimento,
          senha=0,
      )
      pessoaRepo.cadastraCrianca(usuarioCadastro)
      for c in categorias:
          pessoaRepo.insertCategoriasSelecionadas(usuarioCadastro.idPessoa, c)
  
      token = gerar_token()
      if pessoaRepo.alterarToken(email, token):
          response = RedirectResponse(returnUrl, status.HTTP_302_FOUND)
          response.set_cookie(
              key="auth_token_crianca", value=token, max_age=1800, httponly=True
          )
          return response
      else:
          raise Exception(
              "Não foi possível alterar o token do usuário no banco de dados."
          )

@router.get("/cadastroresponsavel", response_class=HTMLResponse)
# address of the route and type of return
async def getCadastroAdulto(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    return templates.TemplateResponse(
        "kids/cadastro/cadastroResponsavel.html",
        {
            "request": request,
            "usuario": usuario,
        },
    )


@router.post("/cadastroresponsavel", response_class=HTMLResponse)
async def postCadastro(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    email: str = Form(""),
    senha: str = Form(""),
    nome: str = Form(""),
    dataNascimento: date = Form(""),
    crianca: bool = False,
    returnUrl: str = Query("/perfilresponsavel"),
):
      nome = capitalizar_nome_proprio(nome).strip()
      senha = senha.strip()
  
      erros = {}
      # validação do campo nome
      is_not_empty(email, "email", erros)
      is_not_empty(nome, "nome", erros)
      is_person_fullname(nome, "nome", erros)
      # validação do campo email
      
      if is_email(email, "email", erros):
          if pessoaRepo.emailExiste(email):
              add_error("email", "Já existe um usuário cadastrado com este e-mail.", erros)
      # validação do campo senha
      is_not_empty(senha, "senha", erros)
      is_password(senha, "senha", erros)

  
      is_not_empty(dataNascimento, "dataNascimento", erros)
  
      # se tem erro, mostra o formulário novamente
      if len(erros) > 0:
          valores = {}
          valores["nome"] = nome
          valores["email"] = email
          valores['dataNascimento'] = str(dataNascimento)
  
          return templates.TemplateResponse(
              "kids/cadastro/cadastroResponsavel.html",
              {
                  "request": request,
                  "usuario": usuario,
                  "erros": erros,
                  "valores": valores,
              },
          )

      print(erros)
  
      usuarioCadastro = Pessoa(
          idPessoa=0,
          idResponsavel=None,
          nome=nome,
          nomeUsuario=None,
          email=email,
          dataNascimento=dataNascimento,
          senha=obter_hash_senha(senha),
          crianca=crianca
      )

      pessoaRepo.cadastraResponsavel(usuarioCadastro)
  
      token = gerar_token()
      if pessoaRepo.alterarToken(email, token):
          response = RedirectResponse(returnUrl, status.HTTP_302_FOUND)
          response.set_cookie(
              key="auth_token", value=token, max_age=1800, httponly=True
          )
          return response
      else:
          raise Exception(
              "Não foi possível alterar o token do usuário no banco de dados."
          )



@router.get("/precadastro", response_class=HTMLResponse)
# address of the route and type of return
async def getPreCadastroUser(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
):
    # if usuario and pessoaRepo.possuiDependente(usuario.id): 
    #     return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
    # else:
      return templates.TemplateResponse(
          "kids/cadastro/pre_cadastro.html", {"request": request, "usuario": usuario}
      )

@router.get("/souadulto", response_class=HTMLResponse)
# address of the route and type of return
async def getPreCadastroUser(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
):
    # if usuario and pessoaRepo.possuiDependente(usuario.id): 
    #     return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
    # else:
      return templates.TemplateResponse(
          "kids/cadastro/souadulto.html", {"request": request, "usuario": usuario}
      )
    
    
@router.get("/aviso", response_class=HTMLResponse)
# address of the route and type of return
async def getAviso(request: Request):
    return templates.TemplateResponse("kids/cadastro/aviso.html", {"request": request})
