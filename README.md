# MMCC — MatVerse Multi-Domain Coherence & Convergence Engine (vΩ)

MMCC fornece um conjunto mínimo e realista de utilitários para consolidar
métricas de coerência e risco entre diferentes "shards" ou domínios. O
foco desta versão é a **Camada 2 Planetária**, com uma API pequena para
computar Ω a partir de entradas locais e agregar resultados globais.

## Motivação

A fórmula de Ω usada aqui prioriza coerência (Ψ) e estabilidade (Θ),
punindo risco de cauda (CVaR) e permitindo incorporar sinais auxiliares
(`PoLE` e `COG`). Todas as entradas são valores normalizados entre `0` e
`1`, com exceção de `CVaR`, que deve estar na faixa `[0, 1]` quanto menor
melhor.

```
Ω = 0.4·Ψ + 0.3·Θ + 0.2·(1 − CVaR) + 0.05·PoLE + 0.05·COG
```

## Estrutura

- `src/mmcc/metrics.py` – funções puras para cálculo de Ω e validação de
  parâmetros.
- `src/mmcc/planetary.py` – agregador simples para a Camada 2 Planetária,
  consolidando métricas de shards e expondo resumos.
- `src/mmcc/__main__.py` – CLI mínima (`python -m mmcc --input shards.json`)
  que lê um JSON de shards e imprime o resumo global em stdout.
- `examples/shards.sample.json` – exemplo de entrada para a CLI.
- `tests/` – cobertura básica para os cálculos de Ω e agregação.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt
```

## Uso rápido

```bash
python -m mmcc --input examples/shards.sample.json
```

Saída esperada (valores variam conforme o arquivo):

```json
{
  "shard_count": 3,
  "omega_global": 0.9178,
  "omega_min": 0.9015,
  "omega_max": 0.9326,
  "psi_mean": 0.91,
  "theta_mean": 0.9,
  "cvar_mean": 0.07
}
```

## Testes

```bash
python -m pytest
```

## Licença

MIT. Consulte o arquivo `LICENSE`.
