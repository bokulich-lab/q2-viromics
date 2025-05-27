# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import importlib

from q2_types.feature_data import FeatureData, Sequence
from q2_types.metadata import ImmutableMetadata
from q2_types.per_sample_sequences import Contigs
from q2_types.sample_data import SampleData
from qiime2.plugin import Citations, Int, Plugin, Range, Float

import q2_viromics

from q2_viromics.checkv.analysis import checkv_analysis
from q2_viromics.checkv.db import checkv_fetch_db
from q2_viromics.checkv.types import (
    CheckVDBDirFmt,
    ViromicsMetadataDirFmt,
    CheckVDB,
    ViromicsMetadata
)
from q2_viromics.virsorter2 import virsorter2_run, virsorter2_fetch_db
from q2_viromics.virsorter2.types import Virsorter2DbDirFmt, Virsorter2Db

citations = Citations.load("citations.bib", package="q2_viromics")

plugin = Plugin(
    name="viromics",
    version=q2_viromics.__version__,
    website="https://github.com/bokulich-lab/q2-viromics",
    package="q2_viromics",
    description="A QIIME 2 plugin for detecting viral genomes and assessing "
    "their quality.",
    short_description="A QIIME 2 plugin for detecting viral genomes and assessing "
    "their quality.",
    citations=[citations["Caporaso-Bolyen-2024"]],
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
        "sequences": SampleData[Contigs],
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
        ("viruses", SampleData[Contigs]),
        ("proviruses", SampleData[Contigs]),
        ("quality_summary", SampleData[ViromicsMetadata]),
        ("contamination", SampleData[ViromicsMetadata]),
        ("completeness", SampleData[ViromicsMetadata]),
    ],
    output_descriptions={
        "viruses": "Viral sequences.",
        "proviruses": "Proviral sequences.",
        "quality_summary": "Summary of sequence quality, completeness, and "
        "contamination.",
        "contamination": "Details on contamination levels, viral and host genes.",
        "completeness": "Completeness estimates and confidence levels.",
    },
    name="Analysis of viral genomes",
    description="Assessing the quality and completeness of viral genomes.",
    citations=[citations["CheckV"]],
)

plugin.methods.register_function(
    function=virsorter2_fetch_db,
    inputs={},
    parameters={
        "n_jobs": Int % Range(1, None),
    },
    outputs=[("database", Virsorter2Db)],
    parameter_descriptions={
        "n_jobs": "Number of simultaneous downloads.",
    },
    output_descriptions={"database": "Virsorter2 database."},
    name="Fetch virsorter2 database",
    description=(
        "Fetch a Virsorter2 database that includes a collection "
        "of known viral genomes and key genes that are typically "
        "found in viral genomes."
    ),
    citations=[citations["VirSorter2"]],
)

plugin.methods.register_function(
    function=virsorter2_run,
    inputs={
        "sequences": FeatureData[Sequence],
        "database": Virsorter2Db,
    },
    parameters={
        "n_jobs": Int % Range(1, None),
        "min_score": Float % Range(0, 1),
        "min_length": Int % Range(0, None),
    },
    input_descriptions={
        "sequences": "Input sequences from an assembly or genome "
        "data for virus detection.",
        "database": "VirSorter2 database.",
    },
    parameter_descriptions={
        "n_jobs": "Max number of jobs allowed in parallel.",
        "min_score": "Minimal score to be identified as viral.",
        "min_length": "Minimal sequence length required. All sequences "
        "shorter than this will "
        "be removed.",
    },
    outputs=[
        ("viral_sequences", FeatureData[Sequence]),
        ("viral_score", ImmutableMetadata),
        ("viral_boundary", ImmutableMetadata),
    ],
    output_descriptions={
        "viral_sequences": "Identified viral sequences.",
        "viral_score": "Viral score table.",
        "viral_boundary": "Viral boundary table.",
    },
    name="Identify viral sequences and produce corresponding metadata",
    description="Performs analysis for identifying and categorizing viral "
    "sequences from metagenomic data using VirSorter2 and provides "
    "corresponding metadata data.",
    citations=[citations["VirSorter2"]],
)

plugin.register_formats(
    CheckVDBDirFmt,
    ViromicsMetadataDirFmt,
    Virsorter2DbDirFmt
)

plugin.register_semantic_types(CheckVDB, ViromicsMetadata, Virsorter2Db)

plugin.register_artifact_class(
    CheckVDB,
    directory_format=CheckVDBDirFmt,
    description=("CheckV database."),
)

plugin.register_semantic_type_to_format(
    SampleData[ViromicsMetadata],
    directory_format=ViromicsMetadataDirFmt,
)

plugin.register_artifact_class(
    Virsorter2Db,
    directory_format=Virsorter2DbDirFmt,
    description=("VirSorter2 database."),
)

importlib.import_module("q2_viromics.checkv.types._transformer")
