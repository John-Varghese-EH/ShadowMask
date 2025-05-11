# tests/test_core.py

from shadowmask.core import apply_alpha_attack

def test_apply_alpha_attack():
    result = apply_alpha_attack("test.jpg")
    assert result.endswith("_alpha.png")
