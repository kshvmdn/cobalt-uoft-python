from setuptools import setup

setup(
    name='cobaltuoft',
    version='0.0.5',
    description='A wrapper for the Cobalt API.',
    long_description='A Python library for interfacing with Cobalt (http://cobalt.qas.im), a University of Toronto Open Data API.',
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
    keywords=['cobalt', 'uoft', 'university of toronto', 'api wrapper', 'open data'],
    packages=[
        'cobaltuoft',
        'cobaltuoft.endpoints',
        'cobaltuoft.helpers',
        'cobaltuoft.helpers.scrapers'
    ],
    package_data={
        '': ['LICENSE']
    },
    package_dir={'cobaltuoft': 'cobaltuoft'},
    install_requires=['requests', 'bs4'],
    include_package_data=True
)
