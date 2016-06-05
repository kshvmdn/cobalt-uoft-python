from setuptools import setup

setup(
    name='cobaltuoft',
    version='0.1.0',
    description='A Python Cobalt library.',
    long_description='A Python wrapper for interfacing with Cobalt, open data APIs and datasets for the University of Toronto.',
    url='https://github.com/kshvmdn/cobalt-uoft-python',
    author='Kashav Madan',
    author_email='kshvmdn@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=[
        'cobalt',
        'uoft',
        'university of toronto',
        'api wrapper',
        'open data'
    ],
    packages=[
        'cobaltuoft',
        'cobaltuoft.helpers',
        'cobaltuoft.helpers.scrapers'
    ],
    package_data={
        '': ['LICENSE']
    },
    package_dir={
        'cobaltuoft': 'cobaltuoft'
    },
    install_requires=[
        'bs4',
        'requests'
    ],
    include_package_data=True
)
