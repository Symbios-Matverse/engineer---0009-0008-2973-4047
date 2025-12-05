"""Camada 2 Planetária: agregação de métricas entre shards.

A intenção é fornecer um ponto único para consolidar métricas locais,
retornando tanto um Ω global quanto estatísticas auxiliares que ajudam a
monitorar coerência e risco em rede.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List

from .metrics import OmegaInputs, average, compute_omega


@dataclass
class ShardMetrics:
    name: str
    psi: float
    theta: float
    cvar: float
    pole: float = 0.0
    cog: float = 0.0

    def as_inputs(self) -> OmegaInputs:
        inputs = OmegaInputs(
            psi=self.psi,
            theta=self.theta,
            cvar=self.cvar,
            pole=self.pole,
            cog=self.cog,
        )
        inputs.assert_valid()
        return inputs.clamped()

    def omega(self) -> float:
        return compute_omega(self.as_inputs())


@dataclass
class PlanetaryLayer:
    shards: List[ShardMetrics] = field(default_factory=list)

    def add_shard(self, shard: ShardMetrics) -> None:
        self.shards.append(shard)

    def summary(self) -> dict:
        if not self.shards:
            raise ValueError("Nenhum shard registrado para sumarização")

        omega_values = [s.omega() for s in self.shards]
        inputs_list = [s.as_inputs() for s in self.shards]
        psi_values = [i.psi for i in inputs_list]
        theta_values = [i.theta for i in inputs_list]
        cvar_values = [i.cvar for i in inputs_list]

        mean_inputs = OmegaInputs(
            psi=average(psi_values),
            theta=average(theta_values),
            cvar=average(cvar_values),
            pole=average([i.pole for i in inputs_list]),
            cog=average([i.cog for i in inputs_list]),
        )

        return {
            "shard_count": len(self.shards),
            "omega_global": compute_omega(mean_inputs),
            "omega_min": min(omega_values),
            "omega_max": max(omega_values),
            "psi_mean": mean_inputs.psi,
            "theta_mean": mean_inputs.theta,
            "cvar_mean": mean_inputs.cvar,
        }

    @classmethod
    def from_json(cls, path: Path | str) -> "PlanetaryLayer":
        data = json.loads(Path(path).read_text())
        if not isinstance(data, list):
            raise TypeError("Arquivo JSON deve conter uma lista de shards")
        if not data:
            raise ValueError("Lista de shards vazia no arquivo JSON")
        shards = [
            ShardMetrics(
                name=item["name"],
                psi=item["psi"],
                theta=item["theta"],
                cvar=item["cvar"],
                pole=item.get("pole", 0.0),
                cog=item.get("cog", 0.0),
            )
            for item in data
        ]
        return cls(shards=shards)


def to_json_summary(layer: PlanetaryLayer) -> str:
    return json.dumps(layer.summary(), indent=2, sort_keys=True)
