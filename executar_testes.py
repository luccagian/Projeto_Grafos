"""
Integrantes:
Gabriel Medina - 10426931
Gian Lucca Campanha Ribeiro - 10438361
Lucas Carmo - 10439830

Arquivo: executar_testes.py
Resumo: Executa todos os testes do projeto.

Histórico de alterações:
    2026-09-30 | Gian Lucca Campanha Ribeiro | Adição do arquivo ao repositório (upload).
    2026-10-01 | Gian Lucca Campanha Ribeiro | Adição do arquivo ao repositório (upload).
    2026-10-28 | Gian Lucca Campanha Ribeiro | Refatoração da estrutura do projeto em pastas.
    2026-10-28 | Gian Lucca Campanha Ribeiro | Refatoração, visualização PyVis e pesos em km (Haversine).
    2026-11-19 | Gabriel Medina | Inclusão dos testes das análises da Parte 3 na suíte.
"""

import unittest

from testes.testeProjeto import TesteProjeto
from testes.testeExercicios import TesteExercicios
from testes.testeAnalises import TesteResiliencia, TesteCaracteristicas, TesteRedeReal


def montar_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TesteExercicios))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TesteProjeto))
    for caso in (TesteResiliencia, TesteCaracteristicas, TesteRedeReal):
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(caso))
    return suite


if __name__ == "__main__":
    resultado = unittest.TextTestRunner(verbosity=2).run(montar_suite())
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
