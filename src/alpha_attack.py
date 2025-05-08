import argparse
import numpy as np
from PIL import Image
import sys
import os

def open_and_prepare_image(path, size=None):
    """Open an image, convert to RGBA, and resize if needed."""
    img = Image.open(path).convert("RGBA")
    if size and img.size != size:
        img = img.resize(size, Image.LANCZOS)
    return img

def alpha_layer_attack(visible_img_path, ai_img_path, output_path, preview=False):
    if not os.path.exists(visible_img_path):
        print(f"Error: {visible_img_path} does not exist.")
        sys.exit(1)
    if not os.path.exists(ai_img_path):
        print(f"Error: {ai_img_path} does not exist.")
        sys.exit(1)

    # Open images and ensure same size
    visible_img = open_and_prepare_image(visible_img_path)
    ai_img = open_and_prepare_image(ai_img_path, visible_img.size)

    # Convert to numpy arrays
    visible_np = np.array(visible_img).astype(np.float32) / 255.0
    ai_np = np.array(ai_img).astype(np.float32) / 255.0

    # Calculate alpha channel for each pixel (per channel)
    # Avoid division by zero
    mask = (1 - ai_np[..., :3]) != 0
    alpha = np.ones_like(visible_np[..., 0])
    alpha[mask.any(axis=-1)] = (
        (1 - visible_np[..., :3])[mask].mean(axis=-1) / (1 - ai_np[..., :3])[mask].mean(axis=-1)
    )
    alpha = np.clip(alpha, 0, 1)

    # Compose output image: RGB from ai_img, alpha from computed alpha
    output_np = np.zeros_like(visible_np)
    output_np[..., :3] = ai_np[..., :3]
    output_np[..., 3] = alpha

    # Convert back to image
    output_img = Image.fromarray((output_np * 255).astype(np.uint8), mode="RGBA")
    output_img.save(output_path)
    print(f"Output saved to {output_path}")

    if preview:
        visible_img.show(title="Visible Image")
        ai_img.show(title="AI Image")
        output_img.show(title="Output (Alpha Attack)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advanced Alpha Layer Attack: Cloak images from AI while keeping them human-readable."
    )
    parser.add_argument("visible_img", help="Path to image for human eyes")
    parser.add_argument("ai_img", help="Path to image for AI systems")
    parser.add_argument("output_img", help="Output PNG path")
    parser.add_argument("--preview", action="store_true", help="Preview images before and after processing")
    args = parser.parse_args()

    alpha_layer_attack(args.visible_img, args.ai_img, args.output_img, preview=args.preview)
