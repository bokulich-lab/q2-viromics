# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.feature_data import FeatureData, Sequence
from q2_types.metadata import ImmutableMetadata
from qiime2.plugin import Citations, Int, Plugin, Range

from q2_viromics import __version__
from q2_viromics.checkv_analysis import checkv_analysis
from q2_viromics.checkv_fetch_db import checkv_fetch_db
from q2_viromics.types._format import CheckVDBDirFmt, GenomadDBDirFmt
from q2_viromics.types._type import CheckVDB, GenomadDB

citations = Citations.load("citations.bib", package="q2_viromics")

plugin = Plugin(
    name="viromics",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-viromics",
    package="q2_viromics",
    description="A QIIME 2 plugin for evaluating viral genome quality "
    "and completeness from metagenomes and removing "
    "host contamination.",
    short_description="A QIIME 2 plugin for detecting viral genomes and assessing "
    "their quality.",
    citations=[citations["Caporaso-Bolyen-2024"]],
)

plugin.register_formats(
    CheckVDBDirFmt,
    GenomadDBDirFmt,
)

plugin.register_semantic_types(CheckVDB, GenomadDB)

plugin.register_artifact_class(
    CheckVDB,
    directory_format=CheckVDBDirFmt,
    description=("CheckV database."),
)

plugin.register_artifact_class(
    GenomadDB,
    directory_format=GenomadDBDirFmt,
    description=("Genomad database."),
)


plugin.methods.register_function(
    function=checkv_fetch_db,
    inputs={},
    parameters={},
    outputs=[("database", CheckVDB)],
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

plugin.methods.register_function(
    function=checkv_analysis,
    inputs={
        "sequences": FeatureData[Sequence],
        "database": CheckVDB,
    },
    parameters={
        "num_threads": Int % Range(1, None),
    },
    input_descriptions={
        "sequences": "Input sequences.",
        "database": "CheckV database.",
    },
    parameter_descriptions={
        "num_threads": "Number of threads to use for prodigal-gv and DIAMOND.",
    },
    outputs=[
        ("viruses", FeatureData[Sequence]),
        ("proviruses", FeatureData[Sequence]),
        ("quality_summary", ImmutableMetadata),
        ("contamination", ImmutableMetadata),
        ("completeness", ImmutableMetadata),
        ("complete_genomes", ImmutableMetadata),
    ],
    output_descriptions={
        "viruses": "Viral sequences.",
        "proviruses": "Proviral sequences.",
        "quality_summary": "Summary of sequence quality, completeness, and "
        "contamination.",
        "contamination": "Details on contamination levels, viral and host genes.",
        "completeness": "Completeness estimates and confidence levels.",
        "complete_genomes": "Complete genomes with predictions.",
    },
    name="Analysis of viral genomes",
    description="Assessing the quality and completeness of viral genomes.",
    citations=[citations["CheckV"]],
)
