# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin import Citations, Plugin

from q2_viromics import __version__
from q2_viromics.types._format import CheckVDBDirFmt
from q2_viromics.types._type import CheckVDB

citations = Citations.load("citations.bib", package="q2_viromics")

plugin = Plugin(
    name="viromics",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-viromics",
    package="q2_viromics",
    description="A QIIME 2 plugin for assessing the quality and completeness of "
    "metagenome-assembled viral genomes.",
    short_description="A QIIME 2 plugin for assessing the quality and completeness "
    "of metagenome-assembled viral genomes.",
    citations=[citations["Caporaso-Bolyen-2024"]],
)

plugin.register_formats(
    CheckVDBDirFmt,
)

plugin.register_semantic_types(CheckVDB)

plugin.register_artifact_class(
    CheckVDB,
    directory_format=CheckVDBDirFmt,
    description=("CheckV database."),
)
