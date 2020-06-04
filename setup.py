import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotframework-wadlibrary",
    version="20.06.04",
    author="Elias Hachichou, Adwisit",
    author_email="elias.hachichou@adwisit.se",
    description="WADLibrary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Adwisit/WADLibrary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
