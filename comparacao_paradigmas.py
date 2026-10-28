from decimal import Decimal
from functools import reduce

from funcoes_puras import MULTA_DIARIA, calcular_dias_atraso, calcular_multa, esta_ativo_e_atrasado


def total_multas_imperativo(emprestimos, data_referencia, valor_diario=MULTA_DIARIA):
    total = Decimal("0.00")
    for emprestimo in emprestimos:
        if emprestimo.ativo:
            dias = (data_referencia - emprestimo.data_prevista_devolucao).days
            if dias > 0:
                total = total + calcular_multa(dias, valor_diario)
    return total


def total_multas_funcional(emprestimos, data_referencia, valor_diario=MULTA_DIARIA):
    atrasados = filter(lambda emprestimo: esta_ativo_e_atrasado(emprestimo, data_referencia), emprestimos)
    multas = map(lambda emprestimo: calcular_multa(calcular_dias_atraso(emprestimo, data_referencia), valor_diario), atrasados)
    return reduce(lambda acumulado, multa: acumulado + multa, multas, Decimal("0.00"))


def comparar_paradigmas(emprestimos, data_referencia, valor_diario=MULTA_DIARIA):
    imperativo = total_multas_imperativo(emprestimos, data_referencia, valor_diario)
    funcional = total_multas_funcional(emprestimos, data_referencia, valor_diario)
    return imperativo, funcional, imperativo == funcional
