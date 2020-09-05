from setuptools import setup

setup(
    name='evkit',
    version='0.10.0',
    packages=[''],
    url='https://github.com/lialkaas/evkit',
    license='MIT',
    author='Oleksii Lialka',
    author_email='lialka@ualberta.ca',
    description='App for extracting and parsing \
        SEC Financial Statement Data Set, \
        equity valuation, discovery of mispriced equities.',
    install_requires=['pandas']
)
