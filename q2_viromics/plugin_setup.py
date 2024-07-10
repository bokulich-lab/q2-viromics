# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin import Citations, Plugin

from q2_viromics import __version__
from q2_viromics.checkv_fetch_db import checkv_fetch_db
from q2_viromics.types._format import CheckVDbDirFmt
from q2_viromics.types._type import CheckVDb

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
    CheckVDbDirFmt,
)

plugin.register_semantic_types(CheckVDb)

plugin.register_artifact_class(
    CheckVDb,
    directory_format=CheckVDbDirFmt,
    description=("CheckV database."),
)


plugin.methods.register_function(
    function=checkv_fetch_db,
    inputs={},
    parameters={},
    outputs=[("database", CheckVDb)],
    parameter_descriptions={},
    output_descriptions={"database": "CheckV database."},
    name="Fetch CheckV database",
    description=(
        "Fetch a CheckV database that includes a comprehensive collection "
        "of complete viral genomes from both cultured isolates "
        "and environmental samples."
    ),
    citations=[citations["CheckV"]],
)
