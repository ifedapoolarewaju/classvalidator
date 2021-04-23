from setuptools import setup, find_packages

import classvalidator


install_requires = ['typing-inspect==0.6.0']

with open('README.md', 'r') as fp:
    long_description = fp.read()


setup(
    name='classvalidator',
    version=classvalidator.__version__,
    url='http://github.com/ifedapoolarewaju/classvalidator/',
    license='MIT',
    author='Ifedapo Olarewaju',
    install_requires=install_requires,
    author_email='ifedapoolarewaju@gmail.com',
    description='Runtime type validation of Dataclass instances',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests.*','tests']),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
