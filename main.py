from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.denunciaRepo import denunciaRepo
# Rotas Room ON #
from routes.roomon.MainRoutes import router as mainRouter
from routes.roomon.CadastrosRoutes import router as cadastroRoomOnRouter
from routes.roomon.ConfiguracoesRoutes import router as configRoomOnRouter
from routes.roomon.PaginasRoutes import router as pagRouter
from routes.roomon.PerfilUsuarioRoutes import router as perfilUserRouter
# Rotas Room KIDS #
from routes.kids.MainRoutes import router as kidsRouter
from routes.kids.CadastroRoutes import router as cadastroRouter
from routes.kids.ConfiguracoesRoutes import router as configRouter
from routes.kids.SalaRoutes import router as salaRouter
from routes.kids.AdmRoutes import router as admRouter
from routes.kids.ResponsavelRoutes import router as responsavelRouter
from routes.kids.SuporteRoutes import router as suporteRouter

import uvicorn

from repositories.salaRepo import salaRepo
from repositories.pessoaRepo import pessoaRepo
from repositories.categoriaRepo import categoriaRepo

#tabelas da sala
salaRepo.tabelaSala()
salaRepo.tabelaParticipacaoSala()

#tabelas Pessoa
pessoaRepo.tabelaPessoa()
pessoaRepo.tabelaPessoaCategoria()
pessoaRepo.tabelaSeguindo()

#Tabelas categoria
categoriaRepo.tabelaCategoria()

#Tabelas denuncia
denunciaRepo.tabelaDenuncia()

app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

app.include_router(kidsRouter)
app.include_router(cadastroRouter)
app.include_router(configRouter)
app.include_router(salaRouter)
app.include_router(admRouter)
app.include_router(mainRouter)
app.include_router(cadastroRoomOnRouter)
app.include_router(configRoomOnRouter)
app.include_router(pagRouter)
app.include_router(perfilUserRouter)
app.include_router(responsavelRouter)
app.include_router(suporteRouter)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
