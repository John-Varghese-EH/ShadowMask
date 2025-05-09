from setuptools import setup, find_packages

setup(
    name="ShadowMask",
    version="1.0.0",
    description="A privacy tool to protect images from AI facial recognition.",
    author="John Varghese",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "kivy",
        "pillow",
        "numpy",
        "torch",
        "torchvision"
    ],
    entry_points={
        "console_scripts": [
            "shadowmask-gui=shadowmask.gui:ShadowMaskApp.run",
        ]
    },
    python_requires=">=3.8",
)
