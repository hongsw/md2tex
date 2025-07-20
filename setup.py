from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="md2x",
    version="2.0.0",
    author="Seungwoo Hong",
    author_email="seungwoo.hong@baryon.ai",
    description="Universal Markdown Converter - Convert MD to LaTeX, PDF, HTML, ArXiv, and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hongsw/md2tex",
    packages=find_packages(),
    package_data={
        'utils': ['*.tex'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Scientific/Engineering",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "markdown>=3.0.0",
        "watchdog>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
        ],
        "full": [
            "pypandoc>=1.6",
            "python-docx>=0.8.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "md2x=md2x:md2x",
            "md2tex=md2tex:md2tex",  # Keep backward compatibility
        ],
    },
)