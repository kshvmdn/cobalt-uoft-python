from setuptools.core import setup

setup(
    name='cobaltuoft',
    version='0.0.1',
    description='A wrapper for the Cobalt API.',
    long_description='A Python library for interfacing with Cobalt\
        (http://cobalt.qas.im), a University of Toronto Open Data API.',
    author='Kashav Madan',
    author_email='kshvmdn@gmail.com',
    url='https://github.com/kshvmdn/cobaltuoft-python',
    packages=[
        'cobaltuoft'
    ],
    package_data={'': ['LICENSE']},
    package_dir={},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False
)
