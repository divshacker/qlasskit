# Copyright 2023-2024 Davide Gessa

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

import qlasskit

setup(
    name="qlasskit",
    version=qlasskit.__version__,
    python_requires=">= 3.8.2",
    description="A python-to-quantum compiler",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Davide Gessa",
    setup_requires="setuptools",
    author_email="gessadavide@gmail.com",
    license="Apache 2.0",
    packages=[
        "qlasskit",
        "qlasskit.boolopt",
        "qlasskit.types",
        "qlasskit.ast2logic",
        "qlasskit.qcircuit",
        "qlasskit.compiler",
        "qlasskit.algorithms",
        "qlasskit.decompiler",
        "qlasskit.tools",
    ],
    zip_safe=False,
    install_requires=["sympy==1.12"],
    extras_require={
        "tweedledum": ["tweedledum==1.1.1"],
        "bqm": ["pyqubo==1.0.5"],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Physics",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/dakk/qlasskit",
    project_urls={
        "Bug Tracker": "https://github.com/dakk/qlasskit/issues/",
        "Documentation": "https://dakk.github.io/qlasskit",
        "Source": "https://github.com/dakk/qlasskit",
    },
)
