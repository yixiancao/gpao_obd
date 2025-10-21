from setuptools import setup, find_packages

setup(
    name='gpao_obd',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A project for generating templates and finding charts from astronomical data.',
    packages=find_packages(where='gpao_obd'),
    package_dir={'': 'gpao_obd'},
    install_requires=[
        'astropy',
        'numpy',
        'matplotlib',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)