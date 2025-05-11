import os
from PIL import Image
import numpy as np

# FGSM requires torch and torchvision
import torch
import torchvision.transforms as T
from torchvision import models

def _output_path(input_path):
    """
    Returns the output path in the format:
    <directory>/<original file name>_ShadowMask-cloaked.<ext>
    """
    dir_, base = os.path.split(input_path)
    name, ext = os.path.splitext(base)
    # Always save as PNG for alpha attack, keep ext for FGSM
    return os.path.join(dir_, f"{name}_ShadowMask-cloaked{ext}")

def alpha_layer_attack(input_path, strength=0.5):
    """
    Alters the alpha channel of a PNG image to disrupt AI recognition.
    Args:
        input_path (str): Path to input PNG image.
        strength (float): 0 (no change) to 1 (fully transparent). Default 0.5.
    Returns:
        output_path (str): Path to saved image.
    """
    img = Image.open(input_path).convert("RGBA")
    r, g, b, a = img.split()
    alpha = np.array(a).astype(np.float32)
    alpha = (alpha * (1 - strength)).clip(0, 255).astype(np.uint8)
    a = Image.fromarray(alpha, mode='L')
    attacked_img = Image.merge("RGBA", (r, g, b, a))
    output_path = _output_path(input_path)
    attacked_img.save(output_path)
    return output_path

def fgsm_attack(input_path, epsilon=2/255, label=None, model=None, device=None):
    """
    Applies FGSM adversarial noise to an image using a pre-trained model.
    Args:
        input_path (str): Path to input image.
        epsilon (float): Attack strength (default: 2/255).
        label (int): Target class index for the attack. If None, uses predicted class.
        model (torch.nn.Module): Pre-trained model. If None, loads ResNet18.
        device (str): 'cpu' or 'cuda'. If None, auto-detect.
    Returns:
        output_path (str): Path to saved image.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if model is None:
        model = models.resnet18(pretrained=True).to(device)
        model.eval()

    orig = Image.open(input_path).convert("RGB")
    transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img = transform(orig).unsqueeze(0).to(device).requires_grad_(True)

    # Get label if not provided
    if label is None:
        with torch.no_grad():
            output = model(img)
            label = output.argmax(dim=1).item()

    criterion = torch.nn.CrossEntropyLoss()
    output = model(img)
    loss = criterion(output, torch.tensor([label], device=device))
    model.zero_grad()
    loss.backward()
    data_grad = img.grad.data

    # FGSM attack
    perturbed_img = img + epsilon * data_grad.sign()
    perturbed_img = torch.clamp(perturbed_img, 0, 1)

    # Unnormalize and convert to PIL
    inv_normalize = T.Normalize(
        mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
        std=[1/0.229, 1/0.224, 1/0.225]
    )
    img_adv = inv_normalize(perturbed_img.squeeze(0)).clamp(0, 1)
    img_adv_pil = T.ToPILImage()(img_adv.cpu())

    output_path = _output_path(input_path)
    img_adv_pil.save(output_path)
    return output_path

# Optional: CLI for quick testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python core.py <mode: alpha|fgsm> <image_path>")
        sys.exit(1)
    mode, img_path = sys.argv[1], sys.argv[2]
    if mode == "alpha":
        out = alpha_layer_attack(img_path)
        print(f"Alpha attack saved: {out}")
    elif mode == "fgsm":
        out = fgsm_attack(img_path)
        print(f"FGSM attack saved: {out}")
    else:
        print("Unknown mode. Use 'alpha' or 'fgsm'.")
