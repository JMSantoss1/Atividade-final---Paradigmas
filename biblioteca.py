from datetime import timedelta
from itertools import count

import funcoes_puras
from emprestimo import Emprestimo
from livro import Livro
from usuario import Usuario


class ErroBiblioteca(Exception):
    pass


class RegistroNaoEncontrado(ErroBiblioteca):
    pass


class MatriculaDuplicada(ErroBiblioteca):
    pass


class LivroIndisponivel(ErroBiblioteca):
    pass


class EmprestimoJaDevolvido(ErroBiblioteca):
    pass


class Biblioteca:
    PRAZO_PADRAO_DIAS = 14

    def __init__(self):
        self.__livros = {}
        self.__usuarios = {}
        self.__emprestimos = {}
        self.__sequencia_livros = count(1)
        self.__sequencia_usuarios = count(1)
        self.__sequencia_emprestimos = count(1)

    def cadastrar_livro(self, titulo, autor, categoria):
        livro = Livro(next(self.__sequencia_livros), titulo, autor, categoria)
        self.__livros[livro.identificador] = livro
        return livro

    def cadastrar_usuario(self, nome, matricula):
        if any(usuario.matricula == matricula.strip() for usuario in self.__usuarios.values()):
            raise MatriculaDuplicada(f"A matrícula {matricula} já está cadastrada.")
        usuario = Usuario(next(self.__sequencia_usuarios), nome, matricula)
        self.__usuarios[usuario.identificador] = usuario
        return usuario

    def consultar_livro(self, identificador):
        if identificador not in self.__livros:
            raise RegistroNaoEncontrado(f"Livro {identificador} não encontrado.")
        return self.__livros[identificador]

    def consultar_usuario(self, identificador):
        if identificador not in self.__usuarios:
            raise RegistroNaoEncontrado(f"Usuário {identificador} não encontrado.")
        return self.__usuarios[identificador]

    def consultar_emprestimo(self, identificador):
        if identificador not in self.__emprestimos:
            raise RegistroNaoEncontrado(f"Empréstimo {identificador} não encontrado.")
        return self.__emprestimos[identificador]

    def listar_livros(self):
        return tuple(self.__livros.values())

    def listar_usuarios(self):
        return tuple(self.__usuarios.values())

    def listar_emprestimos(self):
        return tuple(self.__emprestimos.values())

    def listar_emprestimos_ativos(self):
        return tuple(filter(lambda emprestimo: emprestimo.ativo, self.__emprestimos.values()))

    def listar_emprestimos_do_usuario(self, identificador_usuario):
        self.consultar_usuario(identificador_usuario)
        return tuple(filter(
            lambda emprestimo: emprestimo.usuario.identificador == identificador_usuario,
            self.__emprestimos.values(),
        ))

    def livro_disponivel(self, identificador_livro):
        self.consultar_livro(identificador_livro)
        return not any(
            emprestimo.ativo and emprestimo.livro.identificador == identificador_livro
            for emprestimo in self.__emprestimos.values()
        )

    def registrar_emprestimo(self, identificador_livro, identificador_usuario, data_emprestimo,
                             prazo_dias=PRAZO_PADRAO_DIAS):
        livro = self.consultar_livro(identificador_livro)
        usuario = self.consultar_usuario(identificador_usuario)
        if not self.livro_disponivel(identificador_livro):
            raise LivroIndisponivel(f"O livro '{livro.titulo}' já está emprestado.")
        emprestimo = Emprestimo(
            next(self.__sequencia_emprestimos),
            livro,
            usuario,
            data_emprestimo,
            data_emprestimo + timedelta(days=prazo_dias),
        )
        self.__emprestimos[emprestimo.identificador] = emprestimo
        return emprestimo

    def registrar_devolucao(self, identificador_emprestimo, data_devolucao):
        emprestimo = self.consultar_emprestimo(identificador_emprestimo)
        if not emprestimo.ativo:
            raise EmprestimoJaDevolvido(f"O empréstimo {identificador_emprestimo} já foi devolvido.")
        devolvido = emprestimo.devolvido_em(data_devolucao)
        self.__emprestimos[identificador_emprestimo] = devolvido
        return devolvido

    def buscar_livros_por_categoria(self, categoria):
        return funcoes_puras.filtrar_livros_por_categoria(self.listar_livros(), categoria)

    def consultar_emprestimos_atrasados(self, data_referencia):
        return funcoes_puras.selecionar_emprestimos_atrasados(self.listar_emprestimos(), data_referencia)

    def gerar_relatorio_multas(self, data_referencia):
        return funcoes_puras.gerar_relatorio_multas(self.listar_emprestimos(), data_referencia)

    def gerar_estatisticas(self, data_referencia):
        return funcoes_puras.calcular_estatisticas(
            self.listar_livros(), self.listar_emprestimos(), data_referencia
        )
