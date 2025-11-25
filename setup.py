from setuptools import setup, find_packages

setup(
    name="poof-token-registry",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={"poof_token_registry": ["tokens.yaml"]},
    install_requires=["pyyaml"],
)
