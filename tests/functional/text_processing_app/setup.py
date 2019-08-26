from setuptools import setup, find_packages

setup(
    version='1.0.0',
    name='text_processing_app',
    author='Alexandre Gravier',
    description='A functional test for aiohook',
    packages=find_packages(exclude=('tests', )),
    entry_points={
        'console_scripts':
        ['process_text = textproc.main:cli']},
    install_requires=['aiohook', 'aiofile==1.5.2'])
