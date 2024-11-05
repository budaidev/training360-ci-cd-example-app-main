from setuptools import setup, find_packages

setup(
    name='configuration-manager',
    version='0.1.0',
    description='A simple CLI configuration manager',
    author='Nadai Endre Levente',
    author_email='nnlete@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'configuration-manager=configuration_manager.main:main',
        ],
    },
    install_requires=[
        'training360-example-lib',
    ],
)
