from setuptools import setup, find_packages

INSTALL_REQ = [
    "pandas >= 0.14",
    "numpy >= 1.8",
    "requests >= 2.7.0",
    "valenoq_utils"
]

PACKAGES = [
    "valenoq",
    "valenoq.api",
    "valenoq.pipe",
    "valenoq.pipe.data",
    "valenoq.pipe.algo",
    "valenoq.study"
]

setup(
    name='valenoq',
    version='0.0.5dev',
    description='Python package to interact with valenoq.com RESTful API',
    url='http://github.com/samarkanov/valenoq',
    author='valenoq.com',
    author_email='samarkanov@gmail.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=INSTALL_REQ,
    packages=PACKAGES
)
