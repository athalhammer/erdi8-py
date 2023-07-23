#    erdi8 - a unique identifier scheme and counter that operates on the
#    base-36 alphabet without [0, 1, and l]
#    Copyright (C) 2021  Andreas Thalhammer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='erdi8',
    version='0.4.0',
    url='https://github.com/athalhammer/erdi8',
    author='Andreas Thalhammer',
    author_email='andreas@thalhammer.bayern',
    description='Count according to lower case alphabet and numbers (without ambiguous 0, 1, and l) and always start with a letter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['erdi8'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Other/Nonlisted Topic',
    ],
    python_requires='>=3.8',
    install_requires=[]
)
