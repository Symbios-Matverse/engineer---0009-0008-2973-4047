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


def test_planetary_clamps_out_of_range_values():
    layer = PlanetaryLayer(
        shards=[
            ShardMetrics(name="x", psi=1.4, theta=-0.2, cvar=1.8, pole=2.0, cog=-1.0),
        ]
    )

    summary = layer.summary()

    assert 0.0 <= summary["omega_global"] <= 1.0
    assert 0.0 <= summary["psi_mean"] <= 1.0


def test_planetary_rejects_invalid_json(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text(__import__("json").dumps({"not": "a list"}))

    layer = PlanetaryLayer
    try:
        layer.from_json(path)
    except TypeError as exc:  # expected
        assert "lista" in str(exc)
    else:  # pragma: no cover - defensive guard
        raise AssertionError("from_json deveria rejeitar JSON não-lista")
