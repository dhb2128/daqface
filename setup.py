from setuptools import setup

setup(
    name='daqface',
    version='0.0.1',
    description='a pip-installable package example',
    license='MIT',
    packages=['daqface'],
    author='RoboDoig',
    keywords=['example'],
    install_requires=['scipy', 'numpy', 'PyDAQmx'],
    url='https://github.com/dhb2128/daqface/'
)