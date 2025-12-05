from mmcc.planetary import PlanetaryLayer, ShardMetrics


def test_planetary_summary_from_shards():
    layer = PlanetaryLayer(
        shards=[
            ShardMetrics(name="a", psi=0.9, theta=0.88, cvar=0.07, pole=0.8, cog=0.79),
            ShardMetrics(name="b", psi=0.92, theta=0.91, cvar=0.06, pole=0.82, cog=0.8),
        ]
    )

    summary = layer.summary()

    assert summary["shard_count"] == 2
    assert 0.0 < summary["omega_min"] <= summary["omega_global"] <= summary["omega_max"] <= 1.0
    assert round(summary["psi_mean"], 2) == 0.91
    assert round(summary["cvar_mean"], 2) == 0.07


def test_planetary_from_json(tmp_path):
    data = [
        {"name": "x", "psi": 0.9, "theta": 0.9, "cvar": 0.05},
        {"name": "y", "psi": 0.8, "theta": 0.85, "cvar": 0.1, "pole": 0.7, "cog": 0.6},
    ]
    path = tmp_path / "shards.json"
    path.write_text(__import__("json").dumps(data))

    layer = PlanetaryLayer.from_json(path)
    summary = layer.summary()

    assert summary["shard_count"] == 2
    assert "omega_global" in summary
