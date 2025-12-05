from mmcc.metrics import OmegaInputs, average, compute_omega


def test_compute_omega_balanced_values():
    inputs = OmegaInputs(psi=0.9, theta=0.9, cvar=0.05, pole=0.8, cog=0.75)
    assert compute_omega(inputs) == 0.8975


def test_clamping_and_rounding():
    inputs = OmegaInputs(psi=1.2, theta=-0.1, cvar=1.4)
    assert compute_omega(inputs) == 0.4


def test_average_requires_values():
    try:
        average([])
    except ValueError:
        pass
    else:
        raise AssertionError("Esperava ValueError para média vazia")
