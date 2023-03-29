from setuptools import setup


VERSION = "0.3.0a1"
GITHUB = "https://github.com/izxxr/bplate"
DOCUMENTATION = "https://bplate.readthedocs.io"
LICENSE = "MIT"
PACKAGES = ["bplate"]

with open("README.MD", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()

    while "\n" in REQUIREMENTS:
        REQUIREMENTS.remove("\n")

setup(
    name="bplate",
    author="izxxr",
    version=VERSION,
    license=LICENSE,
    url=GITHUB,
    project_urls={
        "Documentation": DOCUMENTATION,
        "Issue tracker": GITHUB + "/issues",
    },
    description='Tool for storing and generating boilerplates within seconds',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=REQUIREMENTS,
    packages=PACKAGES,
    python_requires='>=3.8.0',
    entry_points={
        "console_scripts": [
            "bplate=bplate.__main__:cli"
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Typing :: Typed',
    ]
)