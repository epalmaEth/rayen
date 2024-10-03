from setuptools import setup

setup(
    name="rayen",
    version="0.0.5",
    author="Jesus Tordesillas",
    author_email="jtordesillas@ethz.ch",
    description="Imposition of Hard Convex Constraints on Neural Networks",
    url="https://github.com/leggedrobotics/rayen",
    project_urls={
        "Homepage": "https://github.com/leggedrobotics/rayen",
        "Bug Tracker": "https://github.com/leggedrobotics/rayen/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorama>=0.4.6",
        "cvxpy>=1.3.1",
        "cvxpylayers>=0.1.6",
        "numpy>=1.24.2",
        "pycddlib>=2.1.6",
        "scipy>=1.10.1",
        "torch>=1.13.1",
        "tqdm>=4.65.0",
    ],
    packages=["rayen"],
    license="BSD License",
    setup_requires=["setuptools"],
)