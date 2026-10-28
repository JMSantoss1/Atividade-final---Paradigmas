from decimal import Decimal
from functools import reduce
from types import MappingProxyType
from typing import NamedTuple

MULTA_DIARIA = Decimal("2.00")


class ItemMulta(NamedTuple):
    identificador_emprestimo: int
    nome_usuario: str
    titulo_livro: str
    dias_atraso: int
    valor: Decimal


class RelatorioMultas(NamedTuple):
    data_referencia: object
    itens: tuple
    total: Decimal


class Estatisticas(NamedTuple):
    livros_por_categoria: MappingProxyType
    emprestimos_por_usuario: MappingProxyType
    emprestimos_ativos: int
    emprestimos_ativos_em_atraso: int
    valor_total_multas: Decimal


def filtrar_livros_por_categoria(livros, categoria):
    categoria_normalizada = categoria.strip().casefold()
    return tuple(filter(lambda livro: livro.categoria.casefold() == categoria_normalizada, livros))


def calcular_multa(dias_atraso, valor_diario):
    return Decimal(max(dias_atraso, 0)) * valor_diario


def calcular_dias_atraso(emprestimo, data_referencia):
    if not emprestimo.ativo:
        return 0
    return max((data_referencia - emprestimo.data_prevista_devolucao).days, 0)


def esta_ativo_e_atrasado(emprestimo, data_referencia):
    return calcular_dias_atraso(emprestimo, data_referencia) > 0


def selecionar_emprestimos_atrasados(emprestimos, data_referencia):
    return tuple(filter(lambda emprestimo: esta_ativo_e_atrasado(emprestimo, data_referencia), emprestimos))


def criar_item_multa(emprestimo, data_referencia, valor_diario):
    dias = calcular_dias_atraso(emprestimo, data_referencia)
    return ItemMulta(
        emprestimo.identificador,
        emprestimo.usuario.nome,
        emprestimo.livro.titulo,
        dias,
        calcular_multa(dias, valor_diario),
    )


def gerar_relatorio_multas(emprestimos, data_referencia, valor_diario=MULTA_DIARIA):
    atrasados = filter(lambda emprestimo: esta_ativo_e_atrasado(emprestimo, data_referencia), emprestimos)
    itens = tuple(map(lambda emprestimo: criar_item_multa(emprestimo, data_referencia, valor_diario), atrasados))
    total = reduce(lambda acumulado, item: acumulado + item.valor, itens, Decimal("0.00"))
    return RelatorioMultas(data_referencia, itens, total)


def contar_livros_por_categoria(livros):
    contagem = reduce(
        lambda acumulado, livro: {**acumulado, livro.categoria: acumulado.get(livro.categoria, 0) + 1},
        livros,
        {},
    )
    return MappingProxyType(contagem)


def contar_emprestimos_por_usuario(emprestimos):
    contagem = reduce(
        lambda acumulado, emprestimo: {
            **acumulado,
            emprestimo.usuario.matricula: acumulado.get(emprestimo.usuario.matricula, 0) + 1,
        },
        emprestimos,
        {},
    )
    return MappingProxyType(contagem)


def contar_emprestimos_ativos(emprestimos):
    return len(tuple(filter(lambda emprestimo: emprestimo.ativo, emprestimos)))


def contar_emprestimos_ativos_em_atraso(emprestimos, data_referencia):
    return len(selecionar_emprestimos_atrasados(emprestimos, data_referencia))


def calcular_estatisticas(livros, emprestimos, data_referencia, valor_diario=MULTA_DIARIA):
    return Estatisticas(
        contar_livros_por_categoria(livros),
        contar_emprestimos_por_usuario(emprestimos),
        contar_emprestimos_ativos(emprestimos),
        contar_emprestimos_ativos_em_atraso(emprestimos, data_referencia),
        gerar_relatorio_multas(emprestimos, data_referencia, valor_diario).total,
    )
