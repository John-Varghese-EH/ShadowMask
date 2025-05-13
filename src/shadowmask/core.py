"""
Core functionality for ShadowMask
"""

import os
from PIL import Image
import numpy as np
from typing import Union, List, Optional
from .attacks import (
    AlphaLayerAttack,
    AdversarialPattern,
    EncoderAttack,
    DiffusionAttack
)

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

class ShadowMask:
    """Main class for ShadowMask functionality"""
    
    def __init__(self):
        self.alpha_attack = AlphaLayerAttack()
        self.adversarial_pattern = AdversarialPattern()
        self.encoder_attack = EncoderAttack()
        self.diffusion_attack = DiffusionAttack()
        
    def protect_image(
        self,
        image_path: Union[str, Image.Image],
        methods: Optional[List[str]] = None,
        output_path: Optional[str] = None,
        intensity: float = 0.5
    ) -> Image.Image:
        """
        Protect an image using specified methods
        
        Args:
            image_path: Path to image or PIL Image object
            methods: List of protection methods to apply
            output_path: Path to save protected image
            intensity: Protection intensity (0.0 to 1.0)
            
        Returns:
            Protected PIL Image
        """
        if methods is None:
            methods = ['alpha_layer', 'adversarial']
            
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = image_path
            
        protected_image = image.copy()
        
        for method in methods:
            if method == 'alpha_layer':
                protected_image = self.alpha_attack.apply(protected_image, intensity)
            elif method == 'adversarial':
                protected_image = self.adversarial_pattern.apply(protected_image, intensity)
            elif method == 'encoder':
                protected_image = self.encoder_attack.apply(protected_image, intensity)
            elif method == 'diffusion':
                protected_image = self.diffusion_attack.apply(protected_image, intensity)
                
        # Add DMI-PROHIBITED metadata
        protected_image.info['DMI-PROHIBITED'] = 'true'
        
        if output_path:
            protected_image.save(output_path, 'PNG')
            
        return protected_image
    
    def batch_protect(
        self,
        input_dir: str,
        output_dir: str,
        methods: Optional[List[str]] = None,
        intensity: float = 0.5
    ) -> List[str]:
        """
        Protect multiple images in a directory
        
        Args:
            input_dir: Directory containing images to protect
            output_dir: Directory to save protected images
            methods: List of protection methods to apply
            intensity: Protection intensity (0.0 to 1.0)
            
        Returns:
            List of paths to protected images
        """
        os.makedirs(output_dir, exist_ok=True)
        protected_paths = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, f'protected_{filename}')
                
                self.protect_image(
                    input_path,
                    methods=methods,
                    output_path=output_path,
                    intensity=intensity
                )
                protected_paths.append(output_path)
                
        return protected_paths

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
