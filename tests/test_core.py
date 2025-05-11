import os
from shadowmask.core import alpha_layer_attack, fgsm_attack

def test_alpha_layer_attack(tmp_path):
    img = tmp_path / "test.png"
    from PIL import Image
    Image.new("RGBA", (10, 10), (255, 0, 0, 255)).save(img)
    out = alpha_layer_attack(str(img))
    assert os.path.exists(out)

def test_fgsm_attack(tmp_path):
    img = tmp_path / "test.png"
    from PIL import Image
    Image.new("RGB", (224, 224), (255, 0, 0)).save(img)
    out = fgsm_attack(str(img))
    assert os.path.exists(out)
