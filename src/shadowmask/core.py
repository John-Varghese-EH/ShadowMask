import os
from PIL import Image, ImageEnhance
import numpy as np

# FGSM requires torch and a model
import torch
import torchvision.transforms as T
from torchvision import models

def alpha_layer_attack(input_path, output_path=None, strength=0.5):
    """
    Alters the alpha channel of a PNG image to disrupt AI recognition.
    Args:
        input_path (str): Path to input PNG image.
        output_path (str): Path to save the attacked image. If None, auto-named.
        strength (float): 0 (no change) to 1 (fully transparent). Default 0.5.
    Returns:
        output_path (str): Path to saved image.
    """
    img = Image.open(input_path).convert("RGBA")
    r, g, b, a = img.split()
    # Reduce alpha channel (increase transparency)
    alpha = np.array(a).astype(np.float32)
    alpha = (alpha * (1 - strength)).clip(0, 255).astype(np.uint8)
    a = Image.fromarray(alpha, mode='L')
    attacked_img = Image.merge("RGBA", (r, g, b, a))
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_alpha{ext}"
    attacked_img.save(output_path)
    return output_path

def fgsm_attack(input_path, output_path=None, epsilon=2/255, label=None, model=None, device=None):
    """
    Applies FGSM adversarial noise to an image using a pre-trained model.
    Args:
        input_path (str): Path to input image.
        output_path (str): Path to save the attacked image. If None, auto-named.
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

    # Preprocess image
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

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_fgsm{ext}"
    img_adv_pil.save(output_path)
    return output_path

# Example CLI usage:
if __name__ == "__main__":
    # Example usage for manual testing
    print("Running alpha_layer_attack on example.png ...")
    alpha_layer_attack("example.png", strength=0.6)
    print("Running fgsm_attack on example.jpg ...")
    fgsm_attack("example.jpg")
