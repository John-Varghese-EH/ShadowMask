import torch
from torchvision import transforms, models
from PIL import Image
import argparse

def fgsm_attack(image, epsilon, data_grad):
    sign_data_grad = data_grad.sign()
    perturbed_image = image + epsilon * sign_data_grad
    perturbed_image = torch.clamp(perturbed_image, 0, 1)
    return perturbed_image

def main(image_path, output_path, epsilon, label_idx):
    model = models.resnet18(pretrained=True)
    model.eval()
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])
    image = Image.open(image_path).convert('RGB')
    image_tensor = preprocess(image).unsqueeze(0)
    image_tensor.requires_grad = True
    output = model(image_tensor)
    label = torch.tensor([label_idx])
    loss = torch.nn.functional.cross_entropy(output, label)
    model.zero_grad()
    loss.backward()
    data_grad = image_tensor.grad.data
    adv_image = fgsm_attack(image_tensor, epsilon, data_grad)
    adv_image_np = adv_image.squeeze().detach().numpy().transpose(1,2,0)
    adv_image_pil = Image.fromarray((adv_image_np * 255).astype(np.uint8))
    adv_image_pil.save(output_path)
    print(f"Adversarial image saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adversarial Pattern Tool (FGSM)")
    parser.add_argument("image", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--epsilon", type=float, default=0.03, help="Perturbation strength")
    parser.add_argument("--label", type=int, required=True, help="Correct label index for the image (ImageNet class index)")
    args = parser.parse_args()
    main(args.image, args.output, args.epsilon, args.label)
