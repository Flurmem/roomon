from dataclasses import asdict
from fastapi import APIRouter, Depends, Form, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from repositories.categoriaRepo import categoriaRepo
from models.pessoa import Pessoa
from models.categoria import Categoria
from models.sala import Sala
from repositories.pessoaRepo import pessoaRepo
from repositories.salaRepo import salaRepo
from models.usuario import Usuario
from typing import List
from datetime import datetime
import json

from util.security import (
    gerar_token,
    validar_usuario_logado,
    verificar_senha,
    validar_crianca_logado,
)
from util.templateFilters import *
from util.validators import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData
    templates.env.filters["id_img"] = formatarIdParaImagem

@router.get("/", response_class=HTMLResponse)
# address of the route and type of return
async def getInicialRoomOn(request: Request):
  
    return templates.TemplateResponse("kids/cadastro/pre_cadastro.html", {"request": request}
    )

@router.get("/inicialkids", response_class=HTMLResponse)
# address of the route and type of return
async def getpagInicialKids(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado),

):
    if crianca:
        salas = salaRepo.obterSalasInfantis()

        categorias = categoriaRepo.lerTodos()
        usuarios = pessoaRepo.obterUsuariosCriança()

        #listas de participantes para cada sala      
        for sala in salas:
            listaParticipantes = []
            participantes = salaRepo.obterParticipantesKids(sala.idSala)
            for participante in participantes:    
                listaParticipantes.append(participante)
            sala.participantes = listaParticipantes

        return templates.TemplateResponse(
            "kids/main/inicial.html", {"request": request, "salas": salas, "categorias":categorias, "crianca": crianca, 
                                       "usuarios":usuarios,}
        )
    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.get("/logindependentes", response_class=HTMLResponse)
# address of the route and type of return
async def getLoginDependentes(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        dependentes = pessoaRepo.obterDependentes(usuario.id)
        return templates.TemplateResponse(
            "kids/main/login_dependentes.html", {"request": request, "usuario": usuario, "dependentes": dependentes}
        )
    else:
        return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.get("/logindependentes/{email:str}", response_class=HTMLResponse)
# address of the route and type of return
async def getLoginDependentes(
    request: Request,
    email:str, 
    usuario: Usuario = Depends(validar_usuario_logado), 
    crianca: Usuario = Depends (validar_crianca_logado), 
):

    token = gerar_token()
    if pessoaRepo.alterarToken(email, token):
        response = RedirectResponse('/inicialkids', status.HTTP_302_FOUND)
        response.set_cookie(
            key="auth_token_crianca", value=token, max_age=7200, httponly=True
        )
        return response
    else:
        raise Exception(
            "Não foi possível alterar o token do usuário no banco de dados."
        )



@router.get("/loginkids", response_class=HTMLResponse)
# address of the route and type of return
async def getLoginKids(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)

    else:
        return templates.TemplateResponse(
            "kids/main/login.html", {"request": request, "usuario": usuario}
        )


@router.post("/loginkids")
async def postLoginKids(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado),
    email: str = Form(""),
    senha: str = Form(""),
    returnUrl: str = Query("/inicialkids"),
):
    email = email.strip().lower()
    senha = senha.strip()

    # validação de dados
    erros = {}
    # validação do campo email
    is_not_empty(email, "email", erros)
    is_email(email, "email", erros)
    if pessoaRepo.emailPertenceCrianca(email):
       add_error("email", "O email pertence a uma criança", erros)
    # validação do campo senha
    is_not_empty(senha, "senha", erros)

    # só checa a senha no BD se os dados forem válidos
    if len(erros) == 0:
        hash_senha_bd = pessoaRepo.obterSenhaDeEmail(email)

        if hash_senha_bd:
          boolSenha = verificar_senha(senha, hash_senha_bd)
          if verificar_senha(senha, hash_senha_bd):
              token = gerar_token()

              if pessoaRepo.alterarToken(email, token):
                  response = RedirectResponse(returnUrl, status.HTTP_302_FOUND)
                  response.set_cookie(
                      key="auth_token", value=token, max_age=7200, httponly=True
                  )
                  return response
              else:
                  raise Exception(
                      "Não foi possível alterar o token do usuário no banco de dados."
                  )
          else:
                add_error("senha", "Senha não confere.", erros)
        else:
            add_error("email", "Usuário não cadastrado.", erros)

    # se tem algum erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["email"] = email
        return templates.TemplateResponse(
            "kids/main/login.html",
            {
                "request": request,
                "crianca": crianca,
                "erros": erros,
                "valores": valores,
            },
        )


@router.get("/logoutkids")
async def getLogout(request: Request):
    response = RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
    response.set_cookie(
        key="auth_token_crianca", value="", httponly=True, max_age=1800, expires="1970-01-01T00:00:00Z"
    )
    return response




@router.get("/perfilkids/{idUsuario:int}/{idSeguido:int}/{opcao:str}", response_class=HTMLResponse)
async def getPerfilKidsSeguir(
    request: Request,
    idUsuario:int,
    idSeguido:int,  
    opcao: str,
    usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado)
):

    if crianca:
        if opcao == 'seguir':
            return JSONResponse({"ok": pessoaRepo.seguir(idUsuario, idSeguido)})
        elif opcao == 'bloquear':
            return JSONResponse({"ok": pessoaRepo.bloquear(idUsuario, idSeguido)})
        else:
            return JSONResponse({"ok": pessoaRepo.deletarSeguindo(idUsuario, idSeguido)})

    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)



@router.get("/perfilkids/{nomeUsuario:str}", response_class=HTMLResponse)
# address of the route and type of return
async def getPerfilKids(
    request: Request,
    nomeUsuario: str,
    usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado)
):
    if crianca: 
        perfilCrianca = pessoaRepo.obterUsuarioPorNomedoUsuario(nomeUsuario)

        relacao = pessoaRepo.obterRelacaoUsuarios(perfilCrianca.id, crianca.id)

        seguidores= int(pessoaRepo.obterQtdeSeguidores(perfilCrianca.id))
        seguindo= int(pessoaRepo.obterQtdeSeguindo(perfilCrianca.id))
        perfisKids = pessoaRepo.obterUsuariosCriançaParaSeguir(crianca.id)
        salasParticipadas = salaRepo.obterSalasParticipadas(perfilCrianca.id)

        return templates.TemplateResponse(
            "kids/main/perfil.html",
            {
                "request": request,
                "crianca": crianca,
                "seguidores": seguidores,
                "seguindo": seguindo,
                "perfis": perfisKids,
                "perfilCrianca": perfilCrianca,
                "relacao": relacao,
                "salasParticipadas": salasParticipadas,
            },
        )

    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)
        

@router.get("/sidebar", response_class=JSONResponse)
async def getUsuarios(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado),

):
    usuarios = pessoaRepo.obterUsuariosCriança()

    # Convertendo a lista de usuários para um formato JSON serializável
    usuarios_json = [asdict(user) for user in usuarios]

    return JSONResponse({"usuarios": usuarios_json})

@router.get("/verificaadmin", response_class=JSONResponse)
async def getUsuarios(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado),

):
    admin = pessoaRepo.verificaAdmin(usuario.id)
    return JSONResponse({"admin": admin})