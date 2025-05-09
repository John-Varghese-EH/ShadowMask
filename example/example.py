from shadowmask.core import alpha_layer_attack, adversarial_pattern_attack

# Example usage
alpha_layer_attack("visible_image.png", "ai_image.png", "output_alpha.png")
adversarial_pattern_attack("input.jpg", "output_adv.jpg", epsilon=0.03, label_idx=0)
