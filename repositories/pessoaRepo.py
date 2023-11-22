from typing import List
from util.DataBase import Database
from models.pessoa import Pessoa
from models.usuario import Usuario, Relacao


class pessoaRepo:
    @classmethod
    def tabelaPessoa(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS pessoa (
            idPessoa INTEGER PRIMARY KEY AUTOINCREMENT,
            idResponsavel INTEGER,
            nome TEXT NOT NULL,
            nomeUsuario TEXT NOT NULL,
            email TEXT NOT NULL,
            descricao TEXT,
            dataNascimento DATE,
            senha TEXT NOT NULL,
            token TEXT,
            admin BOOLEAN NOT NULL DEFAULT 0,
            crianca BOOLEAN NOT NULL DEFAULT 0,
            UNIQUE (email),
            CONSTRAINT fkidResponsavel FOREIGN KEY (idResponsavel) REFERENCES pessoa(idPessoa) 

        )"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        return cursor.execute(sql).rowcount > 0

    @classmethod
    def tabelaPessoaCategoria(cls):
        sql = """CREATE TABLE IF NOT EXISTS pessoaCategoria (
            idPessoaCategoria INTEGER PRIMARY KEY AUTOINCREMENT,
            idPessoa INTEGER,
            idCategoria INTEGER,
            CONSTRAINT fkPessoa FOREIGN KEY(idPessoa) REFERENCES pessoa(idPessoa) ON DELETE CASCADE,
            CONSTRAINT fkCategoria FOREIGN KEY(idCategoria) REFERENCES categoria(idCategoria) ON DELETE CASCADE
        )"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql).rowcount > 0
        conn.close()
        return resultado

    @classmethod
    def tabelaSeguindo(cls):
        sql = """CREATE TABLE IF NOT EXISTS seguindo (
            idSeguindo INTEGER PRIMARY KEY AUTOINCREMENT,
            idSeguidor INTEGER,
            idSeguido INTEGER,
            bloqueado BOOL NOT NULL DEFAULT 0,
            CONSTRAINT fkidSeguidor FOREIGN KEY (idSeguidor) REFERENCES pessoa(idPessoa) ON DELETE CASCADE,
            CONSTRAINT fkidSeguido FOREIGN KEY (idSeguido) REFERENCES pessoa(idPessoa) ON DELETE CASCADE
)"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql).rowcount > 0
        conn.close()
        return resultado

    # CADASTRO
    @classmethod
    def cadastraResponsavel(cls, pessoa: Pessoa) -> Pessoa:
        sql = "INSERT INTO pessoa(idResponsavel, nome, nomeUsuario, email, dataNascimento, senha, crianca) VALUES(?,?,?,?,?,?,?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
            (
                pessoa.idResponsavel,
                pessoa.nome,
                pessoa.nome,
                pessoa.email,
                pessoa.dataNascimento,
                pessoa.senha,
                pessoa.crianca

            ),
        )
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return pessoa
        else:
            return None

    @classmethod
    def lerPerfis(cls) -> List[Pessoa]:
        sql = """SELECT idPessoa, nome, nomeUsuario, email, dataNascimento, senha
        FROM pessoa"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql).fetchall()
        if resultados is not None:
            objetos = [Pessoa(*objeto) for objeto in resultados]
            return objetos
        else:
            return None

    @classmethod
    def insertCategoriasSelecionadas(cls, idPessoa: int, idCategoria: int):
        sql = """INSERT INTO pessoaCategoria(idPessoa, idCategoria) VALUES (?,?)"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idPessoa, idCategoria))

        if resultado is not None:
            conn.commit()
            conn.close()
            return None
        else:
            conn.close()
            return None

    # kids
    @classmethod
    def cadastraCrianca(cls, pessoa: Pessoa) -> Pessoa:
        sql = """INSERT INTO pessoa(idResponsavel, nome, nomeUsuario, email, dataNascimento, senha, crianca) VALUES(?,?,?,?,?,?,?)"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
            (
                pessoa.idResponsavel,
                pessoa.nome,
                pessoa.nomeUsuario,
                pessoa.email,
                pessoa.dataNascimento,
                pessoa.senha,
                True,
            ),
        )

        if resultado.rowcount > 0:
            pessoa.idPessoa = cursor.lastrowid
            conn.commit()
            conn.close()
            return pessoa
        else:
            conn.close()
            return None

    @classmethod
    def edicaoperfilkids(cls, usuario: Usuario) -> Usuario:
        sql = """UPDATE pessoa set nomeUsuario= ?, email = ? , descricao = ? WHERE idPessoa = ?"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
            (
                usuario.nomeUsuario,
                usuario.email,
                usuario.descricao,
                usuario.id,
            ),
        )
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return usuario
        else:
            conn.close()
            return None

    @classmethod
    def edicaoperfilroomon(cls, usuario: Usuario) -> Usuario:
        sql = """UPDATE pessoa set nomeUsuario= ?, email = ? , descricao = ? WHERE idPessoa = ?"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(
            sql,
            (
                usuario.nomeUsuario,
                usuario.email,
                usuario.descricao,
                usuario.id,
            ),
        )
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return usuario
        else:
            conn.close()
            return None

    @classmethod
    def lerPerfisInfantis(cls) -> List[Pessoa]:
        sql = """SELECT idPessoa, idResponsavel, senha, nome, dataNascimento, nomeUsuario, email
        FROM pessoa WHERE crianca = 1 """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql).fetchall()
        conn.close()
        if resultados is not None:
            objetos = [Pessoa(*objeto) for objeto in resultados]
            return objetos
        else:
            return None

    @classmethod
    def lerPerfisIfantis_comCategorias(cls) -> List[Pessoa]:
        sql = """SELECT group_concat(c.nome) FROM pessoaCategoria uc
        JOIN pessoa uk ON uc.idPessoa = uk.idPessoa
        JOIN categoria c ON uc.idCategoria = c.idCategoria
        GROUP BY uk.id
        """
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultados = cursor.execute(sql).fetchall()
        conn.close()
        if resultados is not None:
            dadosUsers = pessoaRepo.lerTodos()
            for dadoUser, lista in zip(dadosUsers, resultados):
                dadoUser.adicionar_listaCategorias(lista[0])
                dadoUser.listaCategorias = (
                    dadoUser.listaCategorias[0]
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                )
            return dadosUsers
        else:
            return None

    @classmethod
    def emailExiste(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM pessoa WHERE email=?)"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        return bool(resultado[0])

    @classmethod
    def emailPertenceCrianca(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM pessoa WHERE email=? and crianca = TRUE)"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        return bool(resultado[0])

    @classmethod
    def verificaResponsavel(cls, email: str) -> bool:
        sql = "SELECT idPessoa FROM pessoa WHERE email=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        return resultado[0]

    @classmethod
    def obterSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT senha FROM pessoa WHERE email=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None

    @classmethod
    def obterUsuarioPorToken(cls, token: str) -> Usuario:
        sql = "SELECT idPessoa, nome, email, admin, nomeUsuario, descricao FROM pessoa WHERE token=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Usuario(*resultado)
            return objeto
        else:
            return None

    @classmethod
    def alterarToken(cls, email: str, token: str) -> bool:
        sql = "UPDATE pessoa SET token=? WHERE email=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, email))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    # Métodos de "Seguindo"

    @classmethod
    def seguir(cls, idSeguidor: int, idSeguido: int):
        sql = """INSERT INTO seguindo(idSeguidor, idSeguido) VALUES (?,?)"""
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idSeguidor, idSeguido))

        if resultado is not None:
            conn.commit()
            conn.close()
            return None
        else:
            conn.close()
            return None

    @classmethod
    def bloquear(cls, idSeguidor: int, idSeguido: int):
        sql = "INSERT INTO seguindo(idSeguidor, idSeguido, bloqueado) VALUES (?,?,?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idSeguidor, idSeguido, True))

        if resultado is not None:
            conn.commit()
            conn.close()
            return None
        else:
            conn.close()
            return None

    @classmethod
    def atualizarBloqueioAoSeguir(cls, idSeguidor: int, idSeguido: int):
        sql = "UPDATE seguindo set bloqueado = 1 where idSeguidor = ? and idSeguidor = ?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, email))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def deletarSeguindo(cls, idPessoa: int, idSeguido: int) -> bool:
        sql = "DELETE FROM seguindo WHERE idSeguidor = ? and idSeguido =?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        resultado = cursor.execute(sql, (idPessoa, idSeguido))
        if resultado.rowcount > 0:
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def obterQtdeSeguindo(cls, idSeguidor: int) -> int:
        sql = "SELECT COUNT(*) FROM seguindo where idSeguidor = ? and bloqueado != 1"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idSeguidor,)).fetchone()
        return int(resultado[0])

    @classmethod
    def obterQtdeSeguidores(cls, idSeguido: int) -> int:
        sql = "SELECT COUNT(*) FROM seguindo where idSeguido = ? and bloqueado != 1"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idSeguido,)).fetchone()
        return int(resultado[0])

    @classmethod
    def obterUsuariosCriançaParaSeguir(cls, idPessoa: int) -> List[Usuario]:
        sql = """SELECT idPessoa, nome, s.idSeguido, s.idSeguidor, admin, nomeUsuario, crianca, s.bloqueado
                FROM pessoa p
                LEFT JOIN seguindo s ON s.idSeguido = p.idPessoa
                WHERE p.idPessoa != ? AND crianca = TRUE"""

        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idPessoa,)).fetchall()
        conexao.close()

        usuarios = []
        for row in resultado:
            usuario = Usuario(
                id=row[0],
                nome=row[1],
                idSeguido=row[2],
                idSeguidor=row[3],
                admin=row[4],
                nomeUsuario=row[5],
                crianca=row[6],
                bloqueado=row[7],
                email=None,
            )
            usuarios.append(usuario)

        return usuarios

    # Métodos que controlam os dependentes e o usuário criança
    @classmethod
    def obterDependentes(cls, idResponsavel: int) -> int:
        sql = "SELECT idPessoa, email, nomeUsuario FROM pessoa where idResponsavel = ? and crianca = 1"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idResponsavel,)).fetchall()
        if resultado:
            dependentes = []
            for dependente in resultado:
                usuario = Usuario(id=dependente[0],
                                      email=dependente[1], 
                                      nome=None, 
                                      nomeUsuario=dependente[2])
                dependentes.append(usuario)
            return dependentes
        else:
            return None

    @classmethod
    def obterCriancaPorToken(cls, token: str) -> Usuario:
        sql = "SELECT idPessoa, nome, email, admin, nomeUsuario, descricao FROM pessoa WHERE token=? and crianca = 1"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Usuario(id=resultado[0], 
                             nome=resultado[1], 
                             email=resultado[2], 
                             admin=resultado[3],
                             nomeUsuario=resultado[4], 
                             descricao=resultado[5])
            return objeto
        else:
            return None

    @classmethod
    def possuiDependente(cls, id) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM pessoa WHERE idResponsavel=?)"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()
        return bool(resultado[0])

    @classmethod
    def possuiMaxDependentes(cls, email) -> bool:
        sql = '''
            SELECT COUNT(*) FROM pessoa
            WHERE idResponsavel = (SELECT idPessoa FROM pessoa WHERE email = ?);
            '''
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        cursor.execute(sql, (email,))
        resultado = cursor.fetchone()
        quantidade_dependentes = resultado[0]
        return quantidade_dependentes >= 3

# Métodos do room kids
    @classmethod
    def obterUsuariosCriança(cls) -> List[Usuario]:
        sql = """SELECT idPessoa, nome, nomeUsuario
                FROM pessoa p
                WHERE crianca = TRUE"""
    
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        resultados = cursor.execute(sql).fetchall()
        conexao.close()
        if resultados is not None:
            usuarios = []
            for resultado in resultados: 
                objeto =Usuario(id=resultado[0], nome=resultado[1], nomeUsuario=resultado[2], email=None)
                usuarios.append(objeto)
            return usuarios
        else:
            return None

    @classmethod
    def obterUsuarioPorNomedoUsuario(cls, nomeUsuario: str) -> Usuario:
        sql = "SELECT idPessoa, nome, email, admin, nomeUsuario, descricao FROM pessoa WHERE nomeUsuario=?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (nomeUsuario,)).fetchone()
        if resultado:
            objeto = Usuario(*resultado)
            return objeto
        else:
            return None
          
    @classmethod
    def obterRelacaoUsuarios(cls, idSeguido: int, idSeguidor:int) -> Relacao:
        sql = "SELECT idSeguindo, idSeguido, idSeguidor, bloqueado FROM seguindo where idSeguido = ? and idSeguidor = ?"
        conexao = Database.createConnection()
        cursor = conexao.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (idSeguido, idSeguidor)).fetchone()
        if resultado:
            objeto = Relacao(idRelacao=resultado[0], idSeguido=resultado[1], idSeguidor=resultado[2], bloqueado=resultado[3])
            return objeto
        else:
            return None