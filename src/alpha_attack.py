import numpy as np
from PIL import Image
import argparse

def create_alpha_attack(visible_img_path, ai_img_path, output_path):
    visible = Image.open(visible_img_path).convert('L')
    ai = Image.open(ai_img_path).convert('L')
    visible = visible.resize(ai.size)
    I_eye = np.array(visible, dtype=np.float32) / 255.0
    I_ai = np.array(ai, dtype=np.float32) / 255.0
    I_ai[I_ai == 1] = 0.999
    alpha = (1 - I_eye) / (1 - I_ai)
    alpha = np.clip(alpha, 0, 1)
    rgb = (I_ai * 255).astype(np.uint8)
    alpha = (alpha * 255).astype(np.uint8)
    rgba = np.stack([rgb, rgb, rgb, alpha], axis=-1)
    out_img = Image.fromarray(rgba, mode='RGBA')
    out_img.save(output_path)
    print(f"Alpha attack image saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alpha Layer Attack Tool")
    parser.add_argument("visible_img", help="Path to image for human eyes")
    parser.add_argument("ai_img", help="Path to image for AI systems")
    parser.add_argument("output_img", help="Output PNG path")
    args = parser.parse_args()
    create_alpha_attack(args.visible_img, args.ai_img, args.output_img)
