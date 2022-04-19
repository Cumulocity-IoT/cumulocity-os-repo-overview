#
# Copyright (c) 2022 Software AG, Darmstadt, Germany and/or its licensors
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    python_requires=">=3.7",
    name='c8y-os-markdown-generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.0.0',
    description='Cumulocity IoT OS Repo Marldown Generator',
    author='Stefan Witschel',
    author_email="Stefan.Witschel@softwareag.com",
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        "mdutils 1.3.1"
    ],
    zip_safe=False)