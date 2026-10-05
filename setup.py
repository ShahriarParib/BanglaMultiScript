import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bangla-multiscript",
    version="1.0.0",
    author="Shahriar",
    author_email="shahriarhossain1837@gmail.com",
    description="High-Throughput Bengali to Natural Avro Banglish & Urban Code-Mixed Alignment Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShahriarParib/BanglaMultiScript",
    project_urls={
        "Bug Tracker": "https://github.com/ShahriarParib/BanglaMultiScript/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "bangla-multiscript=bangla_multiscript.cli:main",
        ],
    },
)
