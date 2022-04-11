from setuptools import find_packages, setup

setup(
    name='Pcrawler',
    version='1.0.0',
    author="Swarfte",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "asyncio",
        "pyppeteer",
    ],
    description="General pyppeteer crawler model"
)
