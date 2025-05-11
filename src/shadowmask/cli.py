import argparse
from .core import alpha_layer_attack, fgsm_attack

def main():
    parser = argparse.ArgumentParser(
        description="ShadowMask: Protect your images from AI recognition."
    )
    parser.add_argument("image", help="Input image file path")
    parser.add_argument(
        "--mode", choices=["alpha", "fgsm", "both"], default="both",
        help="Attack mode: alpha, fgsm, or both (default: both)"
    )
    args = parser.parse_args()
    out = args.image
    if args.mode in ("alpha", "both"):
        out = alpha_layer_attack(out)
        print(f"Alpha attack applied. Saved as: {out}")
    if args.mode in ("fgsm", "both"):
        out = fgsm_attack(out)
        print(f"FGSM attack applied. Saved as: {out}")

if __name__ == "__main__":
    main()
