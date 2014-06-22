from setuptools import setup, find_packages

setup(
    name='trie-join',
    version='0.1.0',

    author='Vasco Visser',
    author_email='vasco.visser@gmail.com',

    packages=['triejoin'],
    url='https://github.com/VascoVisser/trie-join',
    license='MIT',
    
    description='Join string sets with edit distance constraints',
    long_description=open('README.md').read(),
    
    install_requires=[
        "python-Levenshtein >= 0.11.2",
    ],
)


