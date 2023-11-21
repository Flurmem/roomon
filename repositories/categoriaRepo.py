from typing import List
from util.DataBase import Database
from models.categoria import Categoria

class categoriaRepo:
    @classmethod
    def tabelaCategoria(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS categoria(
            idCategoria INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            assuntos TEXT NOT NULL,
            infantil BOOLEAN NOT NULL DEFAULT 0
            )
            """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql)
        conn.commit()
        conn.close()
        return resultado.rowcount > 0

    @classmethod
    def insert(cls, categoria: Categoria) -> Categoria:
        sql = "INSERT INTO categoria(nome, descricao, assuntos) VALUES(?,?,?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql, (categoria.nome, categoria.descricao, categoria.assuntos)
        )
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return categoria
        else:
            return None

    @classmethod
    def update(cls, categoria: Categoria) -> Categoria:
        sql = "UPDATE categoria SET nome = ?, descricao = ? , assuntos = ? WHERE idCategoria = ?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql, (categoria.nome, categoria.descricao, categoria.assuntos, categoria.idCategoria)
        )
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return categoria
        else:
            conn.close()
            return None

    @classmethod
    def delete(cls, idCategoria: int) -> bool:
        sql = "DELETE FROM categoria WHERE idCategoria = ?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idCategoria,))
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def lerTodos(cls) -> List[Categoria]:
        sql = "SELECT idCategoria, nome, descricao, assuntos FROM categoria"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql).fetchall()
        if resultados is not None:
            objetos = [Categoria(*objeto) for objeto in resultados]
            conn.commit()
            conn.close()
            return objetos
        else:
            conn.close()
            return None

    @classmethod
    def lerUm(cls, idCategoria: int) -> List[Categoria]:
        sql = "SELECT idCategoria, nome, descricao, assuntos FROM categoria WHERE idCategoria = ?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idCategoria,)).fetchone()
        objeto = Categoria (*resultado)
        if resultado is not None:
            conn.commit()
            conn.close()
            return objeto
        else:
            conn.close()
            return None
