# ShadowMask

**Your Face, Your Rules – Beyond AI’s Reach**

ShadowMask is an tool to protect your privacy from unauthorized AI-based facial recognition and image scraping. It lets you cloak your images using Alpha Layer Attacks and Adversarial Patterns, making your photos appear normal to humans but confusing or unreadable to AI systems.

---

## Features

- **Alpha Layer Attack:** Alters the transparency (alpha) channel of PNG images to disrupt AI recognition.
- **Adversarial Pattern (FGSM):** Adds subtle, targeted noise to images to fool AI facial recognition.
- **Simple CLI:** Easy-to-use command-line interface.

---

## Installation

> ```bash
> git clone https://github.com/John-Varghese-EH/ShadowMask.git  
> cd shadowmask  
> pip install -r requirements.txt
> ```

---

## Usage

### Alpha Layer Attack

> ```bash
> python src/alpha_attack.py visible_image.png ai_image.png output.png
> ```


### Adversarial Pattern (FGSM)

> ```bash
> python src/adversarial_pattern.py input.jpg output.jpg --label 207
> ```

---

## Inspiration & Credits

ShadowMask is inspired by leading research and pioneering privacy tools:

- **AlphaDog (Alpha Channel Attacks):** Based on the AlphaDog method, which exploits the alpha channel to present different content to humans and AI.
- **Fawkes by SAND Lab, University of Chicago:** [Fawkes](https://sandlab.cs.uchicago.edu/fawkes/) is a groundbreaking image cloaking tool.
- **Adversarial Pattern Attacks:** Grounded in adversarial machine learning research.

Special thanks to the open-source and academic communities for advancing privacy protection in the age of AI.

---

> [!NOTE]
> *For research and personal privacy protection only. Use responsibly.*

---

## Currently a work in progress, but I’d appreciate your support! ☺️
<p align="left">
  <a href="https://buymeacoffee.com/CyberTrinity">
    <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" />
  </a>
  <a href="https://patreon.com/CyberTrinity">
    <img src="https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white" />
  </a>
</p>
