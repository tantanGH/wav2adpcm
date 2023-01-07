import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wav2adpcm",
    version="0.0.6",
    author="tantanGH",
    author_email="tantanGH@github",
    license='MIT',
    description="WAVE format to X680x0 ADPCM format converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tantanGH/wav2adpcm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'wav2adpcm=wav2adpcm.wav2adpcm:main'
        ]
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=["pydub"],
)
