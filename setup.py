from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='erdi8',
    version='0.0.2',
    url='https://github.com/athalhammer/erdi8',
    author='Andreas Thalhammer',
    author_email='andreas@thalhammer.bayern',
    description='Count according to lower case alphabet and numbers (without ambigous 0, 1, and l)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['erdi8'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Other/Nonlisted Topic',
    ],
    python_requires='>=3.6',
    install_requires=[]
)
