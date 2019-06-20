from setuptools import setup

setup(
    name='evkit',
    version='0.8.1',
    packages=[''],
    url='https://github.com/lialkaas/evkit',
    license='MIT',
    author='Oleksii Lialka',
    author_email='lialka@protonamil.com',
    description='Application for unsuervised equity valuations, discovery of mispriced stocks.',
    install_requires=['numpy', 'pandas', 'requests', 'beautifulsoup4']
)
