from setuptools import setup, find_packages

setup(
    name="cryptocore",
    version="1.0.0",
    author="Ivan",
    description="Cryptographic tool for encryption and decryption",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.15.0",
    ],
    entry_points={
        "console_scripts": [
            "cryptocore=cryptocore.main:main",
        ],
    },
    python_requires=">=3.8",
) 
