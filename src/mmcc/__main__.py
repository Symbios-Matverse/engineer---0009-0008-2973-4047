"""CLI mínima para sumarização de shards.

Exemplo de uso:
    python -m mmcc --input examples/shards.sample.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .planetary import PlanetaryLayer, to_json_summary


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MMCC Camada 2 Planetária")
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Arquivo JSON contendo uma lista de shards",
    )
    parsed = parser.parse_args(args=args)

    layer = PlanetaryLayer.from_json(parsed.input)
    summary_json = to_json_summary(layer)
    print(summary_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
