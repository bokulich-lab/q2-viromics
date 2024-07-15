# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup

import versioneer

description = "A QIIME 2 plugin for the identification and analysis of viral sequences."

setup(
    name="q2-viromics",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD-3-Clause",
    packages=find_packages(),
    author="Christos Matzoros",
    author_email="christosmatzoros@gmail.com",
    description=description,
    url="https://github.com/bokulich-lab/q2-viromics",
    entry_points={
        "qiime2.plugins": ["q2_viromics=" "q2_viromics" ".plugin_setup:plugin"]
    },
    package_data={
        "q2_viromics": ["citations.bib"],
        "q2_viromics.tests": [
            "data/*",
            "data/*/*",
            "data/*/*/*",
            "data/*/*/*/*",
            "data/*/*/*/*/*",
            "data/*/*/*/*/*/*",
        ],
    },
    zip_safe=False,
)
