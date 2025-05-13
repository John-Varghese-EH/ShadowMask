"""
Tests for ShadowMask core functionality
"""

import os
import tempfile
import pytest
from PIL import Image
import numpy as np
from shadowmask.core import ShadowMask
from shadowmask.attacks import (
    AlphaLayerAttack,
    AdversarialPattern,
    EncoderAttack,
    DiffusionAttack
)

@pytest.fixture
def sample_image():
    """Create a sample image for testing"""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tmp.name)
        yield tmp.name
    os.unlink(tmp.name)

@pytest.fixture
def shadowmask():
    """Create ShadowMask instance"""
    return ShadowMask()

def test_alpha_layer_attack(sample_image):
    """Test Alpha Layer Attack"""
    attack = AlphaLayerAttack()
    img = Image.open(sample_image)
    protected = attack.apply(img)
    
    assert protected.mode == 'RGBA'
    assert protected.size == img.size
    assert isinstance(protected, Image.Image)

def test_adversarial_pattern(sample_image):
    """Test Adversarial Pattern"""
    attack = AdversarialPattern()
    img = Image.open(sample_image)
    protected = attack.apply(img)
    
    assert protected.mode == img.mode
    assert protected.size == img.size
    assert isinstance(protected, Image.Image)

def test_encoder_attack(sample_image):
    """Test Encoder Attack"""
    attack = EncoderAttack()
    img = Image.open(sample_image)
    protected = attack.apply(img)
    
    assert protected.mode == img.mode
    assert protected.size == img.size
    assert isinstance(protected, Image.Image)

def test_diffusion_attack(sample_image):
    """Test Diffusion Attack"""
    attack = DiffusionAttack()
    img = Image.open(sample_image)
    protected = attack.apply(img)
    
    assert protected.mode == img.mode
    assert protected.size == img.size
    assert isinstance(protected, Image.Image)

def test_shadowmask_initialization():
    """Test ShadowMask class initialization"""
    shadowmask = ShadowMask()
    assert shadowmask is not None

def test_protect_image(sample_image):
    """Test image protection functionality"""
    shadowmask = ShadowMask()
    output_path = sample_image.replace('.png', '_protected.png')
    
    try:
        protected_image = shadowmask.protect_image(
            sample_image,
            methods=['alpha_layer'],
            output_path=output_path,
            intensity=0.5
        )
        assert os.path.exists(output_path)
        assert protected_image is not None
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)

def test_batch_protect(sample_image):
    """Test batch protection functionality"""
    shadowmask = ShadowMask()
    input_dir = os.path.dirname(sample_image)
    output_dir = os.path.join(input_dir, 'protected')
    
    try:
        protected_paths = shadowmask.batch_protect(
            input_dir,
            output_dir,
            methods=['alpha_layer'],
            intensity=0.5
        )
        assert len(protected_paths) > 0
        assert all(os.path.exists(path) for path in protected_paths)
    finally:
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                os.unlink(os.path.join(output_dir, file))
            os.rmdir(output_dir)
