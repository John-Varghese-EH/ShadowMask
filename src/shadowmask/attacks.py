"""
Protection methods for ShadowMask
"""

import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F
from typing import Union, Tuple

class BaseAttack:
    """Base class for all protection methods"""
    
    def apply(self, image: Image.Image, intensity: float = 0.5) -> Image.Image:
        """Apply protection method to image"""
        raise NotImplementedError

class AlphaLayerAttack(BaseAttack):
    """Alpha Layer Attack - Manipulates PNG transparency layers"""
    
    def apply(self, image: Image.Image, intensity: float = 0.5) -> Image.Image:
        # Convert to RGBA if not already
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
            
        # Create random alpha pattern
        alpha = np.array(image.split()[3])
        pattern = np.random.rand(*alpha.shape) * intensity
        alpha = np.clip(alpha * (1 - pattern), 0, 255).astype(np.uint8)
        
        # Apply pattern to critical facial regions
        height, width = alpha.shape
        face_region = slice(height//4, height*3//4), slice(width//4, width*3//4)
        alpha[face_region] = np.clip(alpha[face_region] * (1 - pattern[face_region]), 0, 255)
        
        # Reconstruct image with new alpha
        r, g, b, _ = image.split()
        return Image.merge('RGBA', (r, g, b, Image.fromarray(alpha)))

class AdversarialPattern(BaseAttack):
    """Adversarial Pattern - Creates subtle distortions"""
    
    def apply(self, image: Image.Image, intensity: float = 0.5) -> Image.Image:
        # Convert to numpy array
        img_array = np.array(image)
        
        # Generate adversarial pattern
        pattern = np.random.randn(*img_array.shape) * intensity
        
        # Apply pattern to critical regions
        height, width = img_array.shape[:2]
        face_region = slice(height//4, height*3//4), slice(width//4, width*3//4)
        pattern[face_region] *= 2  # Stronger effect on face
        
        # Add pattern to image
        protected = np.clip(img_array + pattern, 0, 255).astype(np.uint8)
        return Image.fromarray(protected)

class EncoderAttack(BaseAttack):
    """Encoder Attack - Alters image encoding"""
    
    def apply(self, image: Image.Image, intensity: float = 0.5) -> Image.Image:
        # Convert to tensor
        img_tensor = torch.from_numpy(np.array(image)).float() / 255.0
        
        # Create encoding perturbation
        perturbation = torch.randn_like(img_tensor) * intensity
        
        # Apply perturbation
        protected = torch.clamp(img_tensor + perturbation, 0, 1)
        
        # Convert back to image
        protected = (protected.numpy() * 255).astype(np.uint8)
        return Image.fromarray(protected)

class DiffusionAttack(BaseAttack):
    """Diffusion Attack - Tricks generative AI"""
    
    def apply(self, image: Image.Image, intensity: float = 0.5) -> Image.Image:
        # Convert to tensor
        img_tensor = torch.from_numpy(np.array(image)).float() / 255.0
        
        # Create diffusion-like noise
        noise = torch.randn_like(img_tensor) * intensity
        
        # Apply noise in frequency domain
        fft = torch.fft.fft2(img_tensor)
        fft_noise = torch.fft.fft2(noise)
        protected_fft = fft + fft_noise * intensity
        
        # Convert back to spatial domain
        protected = torch.real(torch.fft.ifft2(protected_fft))
        protected = torch.clamp(protected, 0, 1)
        
        # Convert back to image
        protected = (protected.numpy() * 255).astype(np.uint8)
        return Image.fromarray(protected) 
