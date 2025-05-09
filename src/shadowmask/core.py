from PIL import Image
import numpy as np

def alpha_layer_attack(visible_img_path, ai_img_path, output_path):
    """
    Create an image that looks normal to humans but confuses AI by manipulating the alpha channel.
    """
    visible = Image.open(visible_img_path).convert('RGBA')
    ai = Image.open(ai_img_path).convert('RGBA')
    if visible.size != ai.size:
        ai = ai.resize(visible.size)
    visible_np = np.array(visible).astype(np.float32) / 255.0
    ai_np = np.array(ai).astype(np.float32) / 255.0

    # Calculate alpha channel
    mask = (1 - ai_np[..., :3]) != 0
    alpha = np.ones_like(visible_np[..., 0])
    alpha[mask.any(axis=-1)] = (
        (1 - visible_np[..., :3])[mask].mean(axis=-1) / (1 - ai_np[..., :3])[mask].mean(axis=-1)
    )
    alpha = np.clip(alpha, 0, 1)

    output_np = np.zeros_like(visible_np)
    output_np[..., :3] = ai_np[..., :3]
    output_np[..., 3] = alpha

    output_img = Image.fromarray((output_np * 255).astype(np.uint8), mode="RGBA")
    output_img.save(output_path)
    return output_path

def adversarial_pattern_attack(input_path, output_path, epsilon=0.03, label_idx=0):
    """
    Apply a simple adversarial attack (FGSM) to an image.
    """
    import torch
    from torchvision import models, transforms

    model = models.resnet18(pretrained=True)
    model.eval()
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])
    image = Image.open(input_path).convert('RGB')
    image_tensor = preprocess(image).unsqueeze(0)
    image_tensor.requires_grad = True
    output = model(image_tensor)
    label = torch.tensor([label_idx])
    loss = torch.nn.functional.cross_entropy(output, label)
    model.zero_grad()
    loss.backward()
    data_grad = image_tensor.grad.data
    perturbed_image = image_tensor + epsilon * data_grad.sign()
    perturbed_image = torch.clamp(perturbed_image, 0, 1)
    adv_image_np = perturbed_image.squeeze().detach().numpy().transpose(1,2,0)
    adv_image_pil = Image.fromarray((adv_image_np * 255).astype(np.uint8))
    adv_image_pil.save(output_path)
    return output_path
