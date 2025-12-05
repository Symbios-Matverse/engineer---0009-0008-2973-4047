"""MMCC — Camada 2 Planetária.

Fornece utilitários para cálculo de Ω e agregação entre shards. A API é
mantida deliberadamente pequena para favorecer auditabilidade e testes
rápidos.
"""
from .metrics import OmegaInputs, compute_omega
from .planetary import PlanetaryLayer, ShardMetrics, to_json_summary

__all__ = [
    "OmegaInputs",
    "PlanetaryLayer",
    "ShardMetrics",
    "compute_omega",
    "to_json_summary",
]
