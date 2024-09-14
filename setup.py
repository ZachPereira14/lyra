from setuptools import setup, find_packages

setup(
    name='lyra',
    version='1.0',
    author='Zachary Pereira',
    author_email='zacharypereira14@gmail.com',
        description='lyra is a post-processing Python package designed for the analysis and visualizing raw astronomical light curve data.',
    long_description='',
    long_description_content_type='text/markdown',
    url='notyetdeveloped.com',
    license='personal',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'openpyxl',
        'pandas',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Observatioanl Astronomers/Astrophysicists/Data Analysts',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

