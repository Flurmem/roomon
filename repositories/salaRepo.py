from typing import List
from models.sala import Sala
from models.usuario import Usuario
from util.DataBase import Database


class salaRepo:
    @classmethod
    def tabelaSala(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS sala(
            idSala INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            idCategoria INTEGER,
            idDono INTEGER,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            dataCriacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            publica BOOL NOT NULL,
            infantil BOOL NOT NULL,
            CONSTRAINT fkUserSala FOREIGN KEY(idDono) REFERENCES pessoa(idPessoa) ON DELETE CASCADE,
            CONSTRAINT fkCategoriaSala FOREIGN KEY(idCategoria) REFERENCES categoria(idCategoria) ON DELETE CASCADE)
            """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
        )
        conn.commit()
        conn.close()
        return resultado.rowcount > 0

    @classmethod
    def tabelaParticipacaoSala(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS participacaoSala (
            idParticipacao INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            idPessoa INTEGER,
            idSala INTEGER,
            dataEntrada DATETIME DEFAULT CURRENT_TIMESTAMP,
            dataSaida DATETIME TIMESTAMP,
            participa BOOL DEFAULT TRUE,
            CONSTRAINT fkUser FOREIGN KEY(idPessoa) REFERENCES pessoa(idPessoa) ON DELETE CASCADE)
            """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
        )
        conn.commit()
        conn.close()
        return resultado.rowcount > 0

    @classmethod
    def insert(cls, sala: Sala) -> Sala:
        sql = "INSERT INTO sala(idDono, idCategoria, titulo, descricao, publica, infantil) VALUES(?,?,?,?,?,?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        cursor.execute(
            sql,
            (sala.idDono, sala.idCategoria, sala.titulo, sala.descricao, sala.publica, sala.infantil),
        )

        # Verifica se a inserção foi bem-sucedida
        if cursor.rowcount > 0:
            # Obtém o ID da sala recém-inserida
            sala.idSala = cursor.lastrowid
            conn.commit()
            conn.close()
            return sala
        else:
            conn.close()
            return None

    @classmethod
    def update(cls, sala: Sala) -> Sala:
        sql = "UPDATE sala SET titulo = ?, descricao = ? , dataCriacao = ?, publica=? WHERE idSala = ? "
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
            (sala.titulo, sala.descricao, sala.dataCriacao, sala.publica, sala.idSala),
        )
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return sala
        else:
            conn.close()
            return None

    @classmethod
    def delete(cls, idSala: int) -> bool:
        sql = "DELETE FROM sala WHERE idSala = ?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idSala,))
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def obterSalas(cls) -> List[Sala]:
        sql = """SELECT sala.idSala, sala.idDono, sala.idCategoria, sala.titulo, sala.descricao, pessoa.nome, pessoa.nomeUsuario, categoria.nome, sala.dataCriacao, sala.publica
            FROM sala
            INNER JOIN pessoa ON sala.idDono = pessoa.idPessoa
            INNER JOIN categoria ON sala.idCategoria = categoria.idCategoria
            WHERE sala.infantil = 0
            ORDER BY sala.titulo
            LIMIT 0, 6;"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql).fetchall()
        if resultados is not None:
            objetos = [Sala(idSala=objeto[0], 
                            idDono=objeto[1], 
                            idCategoria=objeto[2], 
                            titulo=objeto[3], 
                            descricao=objeto[4], 
                            nomeUsuario=objeto[5], 
                            categoria=objeto[6], 
                            dataCriacao=[7], 
                            publica=objeto[8]) for objeto in resultados]
            conn.commit()
            conn.close()
            return objetos
        else:
            conn.close()
            return None

    @classmethod
    def obterSalasInfantis(cls) -> List[Sala]:
        sql = """SELECT sala.idSala, sala.idDono, sala.idCategoria, sala.titulo, sala.descricao, pessoa.nomeUsuario, categoria.nome, sala.dataCriacao, sala.publica
            FROM sala
            INNER JOIN pessoa ON sala.idDono = pessoa.idPessoa
            INNER JOIN categoria ON sala.idCategoria = categoria.idCategoria
            WHERE sala.infantil = 1
            ORDER BY sala.titulo
            LIMIT 0, 6;"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql).fetchall()
        if resultados is not None:
            objetos = [Sala(idSala=objeto[0], idDono=objeto[1], idCategoria=objeto[2], titulo=objeto[3], descricao=objeto[4], nomeUsuario=objeto[5], categoria=objeto[6], dataCriacao=[7], publica=objeto[8]) for objeto in resultados]
            conn.commit()
            conn.close()
            return objetos
        else:
            conn.close()
            return None

    @classmethod
    def lerUm(cls, idSala: int) -> List[Sala]:
        sql = "SELECT idSala, idDono, titulo, descricao, dataCriacao, publica FROM sala WHERE idSala = ?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idSala,)).fetchone()
        objeto = Sala(*resultado)
        if resultado is not None:
            conn.commit()
            conn.close()
            return objeto
        else:
            conn.close()
            return None

    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Sala]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = """SELECT idSala, idDono, sala.idCategoria, sala.titulo, sala.descricao, pessoa.nomeUsuario, categoria.nome, sala.dataCriacao, sala.publica FROM sala INNER JOIN pessoa on idDono = idPessoa INNER JOIN categoria on sala.idCategoria =
         categoria.idCategoria ORDER BY titulo LIMIT ?,?"""
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultados = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [Sala(idSala=objeto[0], 
                            idDono=objeto[1], 
                            idCategoria=objeto[2], 
                            titulo=objeto[3], 
                            descricao=objeto[4], 
                            nomeUsuario=objeto[5], 
                            categoria=objeto[6], 
                            dataCriacao=[7], 
                            publica=objeto[8]) for objeto in resultados] 
        return objetos

    @classmethod
    def obterPaginaInfantil(cls, pagina: int, tamanhoPagina: int) -> List[Sala]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = """SELECT idSala, idDono, sala.idCategoria, sala.titulo, sala.descricao, pessoa.nomeUsuario, categoria.nome, sala.dataCriacao, sala.publica FROM sala INNER JOIN pessoa on idDono = idPessoa INNER JOIN categoria on sala.idCategoria =
         categoria.idCategoria 
         WHERE sala.infantil = 1
         ORDER BY titulo LIMIT ?,?"""
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultados = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [Sala(idSala=objeto[0], 
                            idDono=objeto[1], 
                            idCategoria=objeto[2], 
                            titulo=objeto[3], 
                            descricao=objeto[4], 
                            nomeUsuario=objeto[5], 
                            categoria=objeto[6], 
                            dataCriacao=[7], 
                            publica=objeto[8]) for objeto in resultados]
        return objetos

    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = """SELECT CEIL(CAST((SELECT COUNT(*) FROM sala INNER JOIN pessoa on idDono = idPessoa INNER JOIN categoria on sala.idCategoria =
         categoria.idCategoria WHERE sala.infantil = 0) AS FLOAT) / ?) AS qtdePaginas"""
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina,)).fetchone()
        return int(resultado[0])

    @classmethod
    def obterQtdePaginasInfantil(cls, tamanhoPagina: int) -> int:
        sql = """SELECT CEIL(CAST((SELECT COUNT(*) FROM sala INNER JOIN pessoa on idDono = idPessoa INNER JOIN categoria on sala.idCategoria =
         categoria.idCategoria WHERE sala.infantil = 1) AS FLOAT) / ?) AS qtdePaginas"""
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina,)).fetchone()
        return int(resultado[0])

    @classmethod
    def adicionaParticipante(cls, idSala: int, idPessoa: int):
        sql = """INSERT INTO participacaoSala(idSala, idPessoa) VALUES (?, ?)"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idSala, idPessoa),)

        if resultado is not None:
            conn.commit()
            conn.close()
            return None
        else:
            conn.close()
            return None

    @classmethod
    def obterDadosDaSalaAPartirdoUsuario(cls, nomeUsuario: int) -> Sala:
        sql = """SELECT idSala, idDono, titulo, nome, nomeUsuario, idCategoria, sala.descricao FROM sala 
        LEFT JOIN pessoa p on p.idPessoa = sala.idDono 
        WHERE nomeUsuario = ? and crianca=TRUE
"""

        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (nomeUsuario,)).fetchone()
        conexao.close()
        dados = Sala( 
                idSala=resultado[0],
                idDono=resultado[1],
                titulo=resultado[2],
                nome=resultado[3],
                nomeUsuario=resultado[4],
                idCategoria=resultado[5],
                descricao=resultado[6],
            )

        return dados

    @classmethod
    def obterParticipantesKids(cls, idSala: int) -> List[Usuario]:
        sql = """SELECT pessoa.idPessoa, nome, nomeUsuario FROM participacaoSala 
        LEFT JOIN pessoa on participacaoSala.idPessoa = pessoa.idPessoa
        WHERE participacaoSala.idSala = ? and crianca=TRUE

"""
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultados = cursor.execute(sql, (idSala,)).fetchall()
        conexao.close()
        usuario = []

        for resultado in resultados:
            dados = Usuario( 
                    id=resultado[0],
                    nome=resultado[1],
                    nomeUsuario=resultado[2],
                    email=None
                )
            usuario.append(dados)

        return usuario

    @classmethod
    def obterSalasParticipadas(cls, idUsuario) -> List[Sala]:
        sql = """SELECT sala.idSala, idDono, sala.idCategoria, titulo, categoria.nome, nomeUsuario ,dataCriacao, publica FROM participacaoSala
            LEFT JOIN sala on sala.idSala = participacaoSala.idSala
            LEFT JOIN categoria on categoria.idCategoria = sala.idCategoria
            LEFT JOIN pessoa on sala.idDono = pessoa.idPessoa
            WHERE participacaoSala.idPessoa = ?
            LIMIT 0, 6;"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql, (idUsuario,)).fetchall()
        if resultados is not None:
            objetos = [Sala(idSala=objeto[0], idDono=objeto[1], idCategoria=objeto[2], titulo=objeto[3], descricao=None, categoria=objeto[4], nomeUsuario=objeto[5], dataCriacao=[6], publica=objeto[7]) for objeto in resultados]
            conn.commit()
            conn.close()
            return objetos
        else:
            conn.close()
            return None
