import os
from shadowmask.core import alpha_layer_attack, adversarial_pattern_attack

def test_alpha_layer_attack(tmp_path):
    # Use two small PNGs for testing
    visible = os.path.join(tmp_path, "visible.png")
    ai = os.path.join(tmp_path, "ai.png")
    out = os.path.join(tmp_path, "out.png")
    # Create dummy images
    from PIL import Image
    Image.new("RGBA", (10, 10), (255, 0, 0, 255)).save(visible)
    Image.new("RGBA", (10, 10), (0, 255, 0, 255)).save(ai)
    alpha_layer_attack(visible, ai, out)
    assert os.path.exists(out)

def test_adversarial_pattern_attack(tmp_path):
    input_img = os.path.join(tmp_path, "input.jpg")
    output_img = os.path.join(tmp_path, "output.jpg")
    from PIL import Image
    Image.new("RGB", (224, 224), (123, 123, 123)).save(input_img)
    adversarial_pattern_attack(input_img, output_img, epsilon=0.01, label_idx=0)
    assert os.path.exists(output_img)
