# ShadowMask 🎭

**Your Face, Your Rules – Beyond AI’s Reach ✨**

ShadowMask is a tool to protect your privacy from unauthorized AI-based facial recognition and image scraping. It lets you cloak your images using Alpha Layer Attacks and Adversarial Patterns, making your photos appear normal to humans but confusing or unreadable to AI systems.

![ShadowMask-App](/docs/ShadowMask_app.png)

---

## Features 🚀

- **Multiple Protection Methods**:
  - Alpha Layer Attack: Manipulates PNG transparency layers
  - Adversarial Pattern: Creates random cosmetic distortions
  - Encoder Attack: Embeds metadata to signal AI scrapers
  - Diffusion Attack: Applies subtle noise patterns

- **User-Friendly Interfaces**:
  - Modern PyQt5 GUI with real-time preview
  - Command-line interface for batch processing
  - Cross-platform support (Windows, Linux, macOS)

---

## Installation 🛠️

### Windows
1. Download the latest `.exe` installer from [Releases](https://github.com/John-Varghese-EH/ShadowMask/releases)
2. Run the installer and follow the setup wizard
3. Launch ShadowMask from the Start Menu

### Linux
1. Download the latest `.AppImage` from [Releases](https://github.com/John-Varghese-EH/ShadowMask/releases)
2. Make it executable:
   ```bash
   chmod +x ShadowMask-*.AppImage
   ```
3. Run the AppImage:
   ```bash
   ./ShadowMask-*.AppImage
   ```

### macOS
1. Download the latest `.dmg` from [Releases](https://github.com/John-Varghese-EH/ShadowMask/releases)
2. Mount the DMG and drag ShadowMask to Applications
3. Launch from Applications or Spotlight

### From Source
```bash
# Clone the repository
git clone https://github.com/John-Varghese-EH/ShadowMask.git
cd ShadowMask

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"
```
---

## Usage 🎯

### GUI Interface
1. Launch ShadowMask:
   ```bash
   shadowmask-gui
   ```
2. Click "Select Image" to choose an image
3. Select protection methods and adjust intensity
4. Click "Protect Image" to process
5. Save the protected image

### Command Line
```bash
# Basic usage
shadowmask input.jpg -o output.png -m all -i 0.7

# Options
-m, --methods    Protection methods (all, alpha, pattern, encoder, diffusion)
-i, --intensity  Protection intensity (0.1-1.0)
-o, --output     Output file path
-v, --verbose    Show detailed progress
```

### Batch Processing
```bash
# Process all images in a directory
shadowmask input_dir/ -o output_dir/ -m all -i 0.7
```
---
## Protection Methods

1. **Alpha Layer Attack**
   - Manipulates PNG transparency layers
   - Preserves image quality while confusing AI
   - Works best with PNG images

2. **Adversarial Pattern**
   - Creates random cosmetic distortions
   - Maintains human perception
   - Effective against most AI systems

3. **Encoder Attack**
   - Embeds metadata to signal AI scrapers
   - Adds DMI-PROHIBITED flag
   - Helps prevent unauthorized scraping

4. **Diffusion Attack**
   - Applies subtle noise patterns
   - Confuses AI recognition
   - Minimal visual impact

---

## Development 🧑🏻‍💻

### Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Check code style
black src/ tests/
flake8 src/ tests/
```

### Building
```bash
# Build package
python -m build

# Build executables
pyinstaller --onefile --windowed src/shadowmask/gui.py
```

---

> [!NOTE]
> *⚠️ This tool is for research and personal privacy protection only. Use responsibly.*

---
## Contributing 🫂

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

---

## Suggestions & Feedback 💡

Have ideas or want to help improve this project?

> - Report issues on [GitHub Issues](https://github.com/John-Varghese-EH/ShadowMask/issues)
> - Start a discussion  
> - Or email me at [cybertrinity01@gmail.com](mailto:cybertrinity01@gmail.com)  

Your feedback is appreciated! 

---

## 🚧 Currently a work in progress, but I’d appreciate your support! ☺️

[![Buy me a Coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/CyberTrinity)
[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://patreon.com/CyberTrinity)
[![Sponsor](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#white)](https://github.com/sponsors/John-Varghese-EH)

---

<a href="https://github.com/John-Varghese-EH/ShadowMask">ShadowMask</a> © 2025 by <a href="https://www.linkedin.com/in/john--varghese/">John Varghese (@Cyber_Trinity) J0X</a>
