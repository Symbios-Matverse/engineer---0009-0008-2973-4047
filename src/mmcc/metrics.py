"""Funções utilitárias para cálculo de métricas do MMCC.

A função principal `compute_omega` aplica a ponderação definida para
coerência (Psi), estabilidade (Theta) e risco (CVaR). Valores opcionais
para PoLE e COG permitem estender o cálculo sem alterar a fórmula de
base.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class OmegaInputs:
    psi: float
    theta: float
    cvar: float
    pole: float = 0.0
    cog: float = 0.0

    def clamped(self) -> "OmegaInputs":
        """Limita valores à faixa [0, 1] para preservar estabilidade.

        CVaR é tratada de forma especial: valores negativos são
        normalizados para 0 e valores acima de 1 são truncados para 1.
        """
        return OmegaInputs(
            psi=_clamp01(self.psi),
            theta=_clamp01(self.theta),
            cvar=_clamp01(self.cvar),
            pole=_clamp01(self.pole),
            cog=_clamp01(self.cog),
        )

    def assert_valid(self) -> None:
        """Garante que todos os campos sejam números finitos.

        O método não altera valores, servindo apenas para sinalizar entradas
        inválidas (por exemplo, strings ou ``nan``). O ajuste para a faixa
        ``[0, 1]`` continua sendo responsabilidade de ``clamped``.
        """
        for field_name, value in (
            ("psi", self.psi),
            ("theta", self.theta),
            ("cvar", self.cvar),
            ("pole", self.pole),
            ("cog", self.cog),
        ):
            if not isinstance(value, (int, float)):
                raise TypeError(f"{field_name} deve ser numérico; recebido {type(value)!r}")
            if value != value or value in (float("inf"), float("-inf")):
                raise ValueError(f"{field_name} não pode ser infinito ou NaN")


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def compute_omega(inputs: OmegaInputs) -> float:
    """Calcula Ω usando a ponderação padrão.

    A saída é arredondada em quatro casas para facilitar comparação
    entre execuções.
    """
    v = inputs.clamped()
    omega = (
        0.4 * v.psi
        + 0.3 * v.theta
        + 0.2 * (1 - v.cvar)
        + 0.05 * v.pole
        + 0.05 * v.cog
    )
    return round(omega, 4)


def average(values: Iterable[float]) -> float:
    """Retorna a média simples de um iterável de floats.

    Dispara ``ValueError`` para coleções vazias, evitando divisões por
    zero e sinalizando ausência de dados.
    """
    total = 0.0
    count = 0
    for v in values:
        total += v
        count += 1
    if count == 0:
        raise ValueError("Nenhum valor recebido para cálculo de média")
    return total / count
