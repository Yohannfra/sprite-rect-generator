import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rect_generator-yohann",
    version="0.1",
    author="Assouline Yohann",
    author_email="yohannassouline@hotmail.fr",
    description="A python gui that auto create sprites rectangles on spritesheets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yohannfra/sprite-rect-generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
