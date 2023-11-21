# routes/ProjetoRoutes.py
from PIL import Image
from io import BytesIO
from fastapi import (
    APIRouter,
    Depends,
    Form,
    Path,
    HTTPException,
    Request,
    status,
    Query,
    UploadFile,
    File
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


@router.get("/edicaoperfilkids", response_class=HTMLResponse)
# address of the route and type of return
async def getPerfilKids(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado), 
    crianca: Usuario = Depends(validar_crianca_logado),
):
    if crianca:
        return templates.TemplateResponse(
            "kids/configuracoes/edicaoperfil.html",
            {"request": request, "crianca": crianca},
        )

    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.post("/edicaoperfilkids", response_class=HTMLResponse)
# address of the route and type of return
async def postEdicaoPerfilKids(
    request: Request,
    crianca: Usuario = Depends(validar_crianca_logado),
    usuario: Usuario = Depends(validar_usuario_logado),
    arquivoImagem: UploadFile = File(...),
):

    erros = {}
    # validação da imagem
    conteudo_arquivo = await arquivoImagem.read()
    imagem = Image.open(BytesIO(conteudo_arquivo))
    if not imagem:
        add_error("arquivoImagem", "Nenhuma imagem foi enviada.", erros)


    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["arquivoImagem"] = arquivoImagem
        return templates.TemplateResponse(
            "projeto/novo.html",
            {
                "request": request,
                "crianca": crianca,
                "erros": erros,
                "valores": valores,
            }
        )

    imagem.save(f"static/imagens/usuarios/avatar{crianca.id:04d}.jpg", "JPEG")
    return RedirectResponse("/perfilkids", status_code=status.HTTP_303_SEE_OTHER)



@router.get("/contakids", response_class=HTMLResponse)
# address of the route and type of return
async def getContaKids(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado), 
    crianca: Usuario = Depends(validar_crianca_logado),
):
    if crianca:
        return templates.TemplateResponse(
            "kids/configuracoes/contakids.html",
            {"request": request, "crianca": crianca},
        )

    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)




@router.post("/contakids", response_class=HTMLResponse)
# address of the route and type of return
async def postContaKids(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado),
    nomeUsuario: str = Form(""),
    email: str = Form(""),
    descricao: str = Form(""),
    returnUrl: str = Query("/contakids"),
):
    if crianca:
        email = email.lower().strip()

        erros = {}
        # validação do campo nome Usuario
        is_not_empty(nomeUsuario, "nomeUsuario", erros)
        # validação do campo email
        is_not_empty(email, "email", erros)
        if is_email(email, "email", erros):
            if pessoaRepo.emailExiste(email):
                add_error("email", "Já existe um aluno cadastrado com este e-mail.", erros)
        # validação do campo descrição
        is_not_empty(descricao, "descricao", erros)

        # se tem erro, mostra o formulário novamente
        if len(erros) > 0:
            valores = {}
            valores["nomeUsuario"] = nomeUsuario
            valores["email"] = email.lower()
            valores["descricao"] = descricao
            return templates.TemplateResponse(
                "kids/configuracoes/contakids.html",
                {
                    "request": request,
                    "usuario": usuario,
                    "crianca": crianca,
                    "erros": erros,
                    "valores": valores,
                },
            )

        usuarioEditado = Usuario(
        id=crianca.id, nome=crianca.nome, email=email, nomeUsuario=nomeUsuario, descricao=descricao
        )
        pessoaRepo.edicaoperfilkids(usuarioEditado)
        return RedirectResponse(returnUrl, status.HTTP_302_FOUND)
    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

