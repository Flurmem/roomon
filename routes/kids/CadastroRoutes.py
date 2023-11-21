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
    email_responsavel: str = Form(""),
    senha: str = Form(""),
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
      senha = senha.strip()
  
      erros = {}
      # validação do campo nome
      is_not_empty(email_responsavel, "email_responsavel", erros)
      if is_email(email_responsavel, "email_responsavel", erros):
          if pessoaRepo.emailExiste(email_responsavel):
              if pessoaRepo.possuiMaxDependentes(email_responsavel):
                  add_error("email_responsavel", "O usuário já possui 3 dependentes cadastrados", erros)
              if pessoaRepo.emailPertenceCrianca(email_responsavel):
                  add_error("email_responsavel", "O email pertece a uma criança", erros)
          else:
              add_error("email_responsavel", "O email não existe", erros)
      is_not_empty(nome, "nome", erros)
      is_person_fullname(nome, "nome", erros)
      # validação do campo email
      is_not_empty(email, "email", erros)
      if is_email(email, "email", erros):
          if pessoaRepo.emailExiste(email):
              add_error("email", "Já existe um usuário cadastrado com este e-mail.", erros)
      # validação do campo senha
      is_not_empty(senha, "senha", erros)
      is_password(senha, "senha", erros)
  
      is_not_empty(nomeUsuario, "nomeUsuario", erros)
  
      is_not_empty(dataNascimento, "dataNascimento", erros)
  
      categoriasLista = categoriaRepo.lerTodos()
      # se tem erro, mostra o formulário novamente
      if len(erros) > 0:
          valores = {}
          valores["nome"] = nome
          valores["email"] = email.lower()
          valores["email_responsavel"] = email_responsavel
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
  
      email_existe = pessoaRepo.emailExiste(email_responsavel)
      if email_existe:
          idResponsavel = pessoaRepo.verificaResponsavel(email_responsavel)
      else:
          return None
  
      usuarioCadastro = Pessoa(
          idPessoa=0,
          idResponsavel=idResponsavel,
          nome=nome,
          nomeUsuario=nomeUsuario,
          email=email,
          dataNascimento=dataNascimento,
          senha=obter_hash_senha(senha),
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



@router.get("/precadastro", response_class=HTMLResponse)
# address of the route and type of return
async def getPreCadastroUser(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario and pessoaRepo.possuiDependente(usuario.id): 
        return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
    else:
      return templates.TemplateResponse(
          "kids/cadastro/pre_cadastro.html", {"request": request, "usuario": usuario}
      )
    

@router.get("/aviso", response_class=HTMLResponse)
# address of the route and type of return
async def getAviso(request: Request):
    return templates.TemplateResponse("kids/cadastro/aviso.html", {"request": request})
