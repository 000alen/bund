import setuptools

setuptools.setup(
    name="bund",
    version="0.0.0",
    packages=["bund"],
    package_data={"": ["importer.template", "package.template"]},
    include_package_data=True,
    python_requires=">=3.10",
)
