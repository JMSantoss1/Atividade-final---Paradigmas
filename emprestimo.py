class Emprestimo:
    def __init__(self, identificador, livro, usuario, data_emprestimo,
                 data_prevista_devolucao, data_devolucao=None):
        if data_prevista_devolucao < data_emprestimo:
            raise ValueError("A data prevista não pode ser anterior ao empréstimo.")
        if data_devolucao is not None and data_devolucao < data_emprestimo:
            raise ValueError("A devolução não pode ser anterior ao empréstimo.")
        self.__identificador = identificador
        self.__livro = livro
        self.__usuario = usuario
        self.__data_emprestimo = data_emprestimo
        self.__data_prevista_devolucao = data_prevista_devolucao
        self.__data_devolucao = data_devolucao

    @property
    def identificador(self):
        return self.__identificador

    @property
    def livro(self):
        return self.__livro

    @property
    def usuario(self):
        return self.__usuario

    @property
    def data_emprestimo(self):
        return self.__data_emprestimo

    @property
    def data_prevista_devolucao(self):
        return self.__data_prevista_devolucao

    @property
    def data_devolucao(self):
        return self.__data_devolucao

    @property
    def ativo(self):
        return self.__data_devolucao is None

    def devolvido_em(self, data_devolucao):
        if not self.ativo:
            raise ValueError("Este empréstimo já foi devolvido.")
        return Emprestimo(
            self.__identificador,
            self.__livro,
            self.__usuario,
            self.__data_emprestimo,
            self.__data_prevista_devolucao,
            data_devolucao,
        )

    def __repr__(self):
        situacao = "ativo" if self.ativo else f"devolvido em {self.__data_devolucao}"
        return (f"Emprestimo(id={self.__identificador}, livro={self.__livro.titulo!r}, "
                f"usuario={self.__usuario.nome!r}, {situacao})")
