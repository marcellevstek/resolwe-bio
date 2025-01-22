import os.path

import setuptools

# Get long description from README.
with open("README.rst", "r") as fh:
    long_description = fh.read()

# Get package metadata from '__about__.py' file.
about = {}
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, "resolwe_bio", "__about__.py"), "r") as fh:
    exec(fh.read(), about)

setuptools.setup(
    name=about["__title__"],
    use_scm_version=True,
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author=about["__author__"],
    author_email=about["__email__"],
    url=about["__url__"],
    license=about["__license__"],
    # Exclude tests from built/installed package.
    packages=setuptools.find_packages(
        exclude=["tests", "tests.*", "*.tests", "*.tests.*"]
    ),
    package_data={
        "resolwe_bio": [
            "descriptors/*.yml",
            "fixtures/*.yaml",
            "kb/migrations/*.sql",
            "migrations/*.sql",
            "processes/**/*.yml",
            "processes/**/*.py",
            "tools/*.py",
            "tools/*.R",
            "tools/*.sh",
        ]
    },
    python_requires=">=3.11, <3.13",
    install_requires=(
        "Django~=5.1",
        "djangorestframework~=3.15.2",
        "django-filter~=24.3",
        "resolwe==43.*",
        "wrapt~=1.17.0",
    ),
    extras_require={
        "docs": [
            "daphne",
            "Sphinx~=8.1.3",
            "sphinx-rtd-theme==3.0.2",
            "pyasn1>=0.6.1",
        ],
        "package": ["twine", "wheel", "check-manifest", "setuptools_scm"],
        "test": [
            "build==1.2.2",
            "black==24.10.0",
            "check-manifest",
            "colorama",
            "django-stubs>=5.1.1",
            "django-filter-stubs>=0.1.3",
            "djangorestframework-stubs[compatible-mypy]>=3.15.2",
            "daphne",
            "flake8>=7.1.1",
            "isort>=5.13.2",
            "mypy>=1.14.1",
            "pydocstyle~=6.3.0",
            "setuptools_scm",
            "six==1.17",
            "tblib>=3.0.0",
            "twine==6.1.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="bioinformatics resolwe bio pipelines dataflow django",
)
