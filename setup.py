import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flying_ioc",
    version="1.0.3",
    author="Asaf Semo, Dmitry Voronenkov",
    author_email="asafsemo@gmail.com",
    description="IoC for Humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ClanPlay/Python_IoC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
