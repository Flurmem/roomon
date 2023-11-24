from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from models.denuncia import Denuncia
from repositories.categoriaRepo import categoriaRepo
from models.websocket import ConnectionManager
from models.usuario import Usuario
from repositories.denunciaRepo import denunciaRepo

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

@router.get("/denuncias", response_class=HTMLResponse)
async def getDenuncias(request: Request,usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):
  if usuario:
    denuncias = denunciaRepo.obterDenuncias(crianca.id)
    return templates.TemplateResponse(
      "kids/suporte/denuncias.html", {"request": request, "usuario": usuario, "crianca": crianca, "denuncias": denuncias})

  else:
    return RedirectResponse("/loginkids", status.HTTP_302_FOUND)

@router.post("/denuncias")
async def postDenuncias(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado),
    titulo: str = Form(""),
    descricao: str = Form(""),

):
    if crianca:
        denuncias = denunciaRepo.obterDenuncias(crianca.id)
        erros = {}
        # validação do campo email
        is_not_empty(titulo, "titulo", erros)
        is_not_empty(descricao, "descricao", erros)


        # se tem algum erro, mostra o formulário novamente
        if len(erros) > 0:
            valores = {}
            valores["titulo"] = titulo
            return templates.TemplateResponse(
                "/kids/suporte/denuncias.html",
                {
                    "request": request,
                    "crianca": crianca,
                    "erros": erros,
                    "valores": valores,
                    "denuncias": denuncias
                },
            )


        denunciaRepo.insert(
            Denuncia(
                id = 0,
                idDenunciante=crianca.id,
                titulo=titulo,
                descricao=descricao,
            )
        )

        return RedirectResponse("/denuncias", status.HTTP_302_FOUND)
    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)



@router.get("/sobrenos", response_class=HTMLResponse)
async def getDenuncias(request: Request,usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):

    return templates.TemplateResponse(
      "kids/suporte/sobrenos.html", {"request": request, "usuario": usuario, "crianca": crianca})


@router.get("/faq", response_class=HTMLResponse)
async def getDenuncias(request: Request,usuario: Usuario = Depends(validar_usuario_logado),
                      crianca: Usuario = Depends(validar_crianca_logado)):
    return templates.TemplateResponse(
      "kids/suporte/faq.html", {"request": request, "usuario": usuario, "crianca": crianca})
