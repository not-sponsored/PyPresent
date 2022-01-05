import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyPresent",
    version="1.0.0",
    author="Hanwen Zuo",
    author_email="HanwenZuo1@gmail.com",
    description="PyPresent - slide presentations from notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/not-sponsored/PyPresent",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['sample/example_notes.txt', 'sample/test.jpg',
                  'sample/output_presentation.pptx']},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["pypresent=PyPresent.app:main"]},
)
