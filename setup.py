#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements-minimal.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="neural-coding-assistant",
    version="0.1.0",
    author="Neural Coding Team",
    author_email="support@neuralcoding.ai",
    description="AI-powered coding assistance with mesh architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rbbirgeco/TOOLS4TIM",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "full": [
            "llama-cpp-python>=0.2.0",
            "torch>=2.0.0",
            "transformers>=4.30.0",
        ],
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0",
            "isort>=5.12",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "neural-coding-assistant=rest_api:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.json", "*.txt"],
    },
)
