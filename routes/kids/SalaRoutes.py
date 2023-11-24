from io import BytesIO
from PIL import Image
from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from models.chat import Mensagem
from repositories.categoriaRepo import categoriaRepo
from models.sala import Sala
from models.websocket import ConnectionManager
from repositories.chatRepo import chatRepo
from repositories.pessoaRepo import pessoaRepo
from repositories.salaRepo import salaRepo
from models.usuario import Usuario
from fastapi import WebSocket, WebSocketDisconnect


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

@router.get("/criacaoroom", response_class=HTMLResponse)
# address of the route and type of return
async def getCriacaoRoomKids(request: Request, 
                             usuario: Usuario = Depends(validar_usuario_logado),
                             crianca: Usuario = Depends(validar_crianca_logado)):

    if crianca:
            salas = salaRepo.obterSalas()
            categorias = categoriaRepo.lerTodos()
            return templates.TemplateResponse(
                "kids/salas/criacao_room.html", {"request": request, "salas": salas, "categorias":categorias, "crianca": crianca,}
        )
    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)


@router.post("/criacaoroom")
async def postCriacaoRoomKids(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado),
    titulo: str = Form(""),
    categoria: int = Form(""),
    arquivoImagem: UploadFile = File(...),
    descricao: str = Form(""),
    publica: bool = Form(""),
    infantil: bool = Form(""),
):
    if crianca:
        categorias = categoriaRepo.lerTodos()
        erros = {}
        # validação do campo email
        is_not_empty(titulo, "titulo", erros)
        is_not_empty(categoria, "categoria", erros)
        is_not_empty(descricao, "descricao", erros)

        # validação da imagem
        conteudo_arquivo = await arquivoImagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
        if not imagem:
            add_error("arquivoImagem", "Nenhuma imagem foi enviada.", erros)

        # se tem algum erro, mostra o formulário novamente
        if len(erros) > 0:
            valores = {}
            valores["titulo"] = titulo
            return templates.TemplateResponse(
                "/kids/salas/criacao_room.html",
                {
                    "request": request,
                    "crianca": crianca,
                    "erros": erros,
                    "valores": valores,
                    "categorias": categorias,
                },
            )

        sala = salaRepo.insert(
            Sala(
                idSala = 0,
                idDono=crianca.id,
                idCategoria=categoria,
                titulo=titulo,
                descricao=descricao,
                publica=publica,
                infantil=infantil
            )
        )
        

        if sala:
            imagem.save(f"static/imagens/salas/capas/capa{sala.idSala:04d}.jpg", "JPEG")
            
            #cria o chat
            chatRepo.criarChat(sala.idSala)
        return RedirectResponse("/listagem", status.HTTP_302_FOUND)
    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)


@router.get("/listagem", response_class=HTMLResponse)
# address of the route and type of return
async def getListagem(
    request: Request,
    pa: int = 1,
    tp: int = 6,
    usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado)
):
    if crianca:
        salas = salaRepo.obterPaginaInfantil(pa, tp)
        totalPaginas = salaRepo.obterQtdePaginas(tp)

        return templates.TemplateResponse(
            "kids/salas/listagem.html",
            {
                "request": request,
                "salas": salas,
                "totalPaginas": totalPaginas,
                "crianca": crianca,
                "paginaAtual": pa,
                "tamanhoPagina": tp,
            },
        )
    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)


@router.get("/salakids/{nomeUsuario:str}", response_class=HTMLResponse)
# address of the route and type of return
async def getSalaPagina(
    request: Request,
    nomeUsuario: str,
    usuario: Usuario = Depends(validar_usuario_logado),
    crianca: Usuario = Depends(validar_crianca_logado)
):
    if crianca:

        sala = salaRepo.obterDadosDaSalaAPartirdoUsuario(nomeUsuario)

        participantes = salaRepo.obterParticipantesKids(sala.idSala)

        #verifica se o usuario ja participa da sala, só então o adiciona
        idsUsuariosParticipantes = {participante.id for participante in participantes}
        if crianca.id not in idsUsuariosParticipantes:
            salaRepo.adicionaParticipante(sala.idSala, crianca.id)
            participantes.append(crianca)

        criador = pessoaRepo.obterUsuarioPorNomedoUsuario(nomeUsuario)
        
        chat = chatRepo.obterChat(sala.idSala)

        return templates.TemplateResponse(
            "kids/salas/sala.html",
            {
                "request": request,
                "crianca": crianca,
                'sala': sala,
                'participantes': participantes,
                'criador': criador,
                'chat': chat,
            },
        )
    else:
        if usuario:
            return RedirectResponse("/logindependentes", status.HTTP_302_FOUND)
        else:
            return RedirectResponse("/loginkids", status.HTTP_302_FOUND)


@router.websocket("/ws/{nomeUsuario}/{idUsuario}/{idSala}/{idChat}")
async def websocket_endpoint(websocket: WebSocket, 
                             nomeUsuario: str,
                             idUsuario: int,
                             idSala: int,
                             idChat: int,):
    await manager.connect(websocket, idSala)
    try: 
        while True:
            message = await websocket.receive_text()
            data = [nomeUsuario, message, idUsuario, idSala]
            if message:
                mensagem = Mensagem(idMensagem=0, idChat=idChat, idEmissor=idUsuario, conteudo=message)
                chatRepo.armazenarMensagem(mensagem)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"{nomeUsuario} has left the chat")


