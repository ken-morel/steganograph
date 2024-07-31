import steganograph
from pathlib import Path
from setuptools import setup

project_dir = Path(__file__).parent

try:
    long_description = (project_dir / "README.md").read_text()
except FileNotFoundError:
    long_description = Path("README.md").read_text()

setup(
    name='steganograph',
    version=steganograph.__version__,
    packages=['steganograph'],
    license="MIT",
    author='ken-morel',
    description='A sample shellsy plugin',
    install_requires=["Pillow"],
    classifiers=[
        # See https://pypi.org/classifiers/
        "Intended Audience :: Developers",
        'Development Status :: 1 - Planning',
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
