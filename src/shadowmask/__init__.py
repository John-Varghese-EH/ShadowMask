"""
ShadowMask - Protect your privacy from AI facial recognition
"""

__version__ = "1.0.0"
__author__ = "John Varghese"
__description__ = "Your Face, Your Rules – Beyond AI's Reach ✨"

from .core import ShadowMask
from .attacks import AlphaLayerAttack, AdversarialPattern, EncoderAttack, DiffusionAttack

__all__ = [
    'ShadowMask',
    'AlphaLayerAttack',
    'AdversarialPattern',
    'EncoderAttack',
    'DiffusionAttack',
]
