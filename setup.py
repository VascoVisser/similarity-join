from setuptools import setup, find_packages

setup(
    name='similarity-join',
    version='0.1.2',

    author='Vasco Visser',
    author_email='vasco.visser@gmail.com',

    packages=['simjoin'],
    url='https://github.com/VascoVisser/similarity-join',
    license='MIT',
    
    description='Join string lists with similarity constraints',
    long_description=open('README.md').read(),
    
    install_requires=[
        "python-Levenshtein >= 0.11.2",
        "pandas" >= "0.13.1",
        "numpy" >= "1.9.1",
    ],
)


