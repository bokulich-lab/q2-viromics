# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import importlib

from q2_types.per_sample_sequences import Contigs
from q2_types.sample_data import SampleData
from qiime2.plugin import Bool, Citations, Float, Int, Plugin, Range

import q2_viromics

from q2_viromics.checkv_analysis import checkv_analysis
from q2_viromics.checkv_fetch_db import checkv_fetch_db
from q2_viromics.genomad_analysis import genomad_analysis
from q2_viromics.genomad_fetch_db import genomad_fetch_db
from q2_viromics.types._format import (
    CheckVDBDirFmt,
    GenomadDBDirFmt,
    ViromicsMetadataDirFmt,
)
from q2_viromics.types._type import CheckVDB, GenomadDB, ViromicsMetadata

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

plugin.register_formats(
    CheckVDBDirFmt,
    GenomadDBDirFmt,
    ViromicsMetadataDirFmt,
)

plugin.register_semantic_types(CheckVDB, GenomadDB, ViromicsMetadata)

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

plugin.register_semantic_type_to_format(
    SampleData[ViromicsMetadata],
    directory_format=ViromicsMetadataDirFmt,
)

plugin.methods.register_function(
    function=genomad_fetch_db,
    inputs={},
    parameters={},
    outputs=[("database", GenomadDB)],
    parameter_descriptions={},
    output_descriptions={"database": "geNomad database."},
    name="Fetch geNomad database",
    description=(
        "Fetch the geNomad database that contains the profiles of the markers "
        "that are used to classify sequences, their taxonomic information and "
        "their functional annotation."
    ),
    citations=[citations["geNomad"]],
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
    function=genomad_analysis,
    inputs={
        "sequences": SampleData[Contigs],
        "database": GenomadDB,
    },
    parameters={
        "num_threads": Int % Range(1, None),
        "splits": Int % Range(0, None),
        "min_score": Float % Range(0, 1),
        "min_number_genes": Int % Range(0, None),
        "conservative_taxonomy": Bool,
    },
    input_descriptions={
        "sequences": "Input sequences.",
        "database": "GeNomad database.",
    },
    parameter_descriptions={
        "num_threads": "Number of threads to use for prodigal-gv and DIAMOND.",
        "splits": "Split the data for the MMseqs2 search. Higher values will "
        "reduce memory usage, but will make the search slower. If the "
        "MMseqs2 search is failing, try to increase the number of splits.",
        "min_score": "Minimum score to flag a sequence as virus or plasmid.",
        "min_number_genes": "The minimum number of genes a sequence must encode to "
        "be considered for classification as a plasmid or virus.",
        "conservative_taxonomy": "Make the virus taxonomic assignment process more "
        "conservative. This might reduce the amount of "
        "genomes assigned to the family level, but will "
        "decrease the rate of family misassignment.",
    },
    outputs=[
        ("viruses", SampleData[Contigs]),
        ("proviruses", SampleData[Contigs]),
        ("plasmid", SampleData[Contigs]),
        ("virus_summary", SampleData[ViromicsMetadata]),
    ],
    output_descriptions={
        "viruses": "Viral sequences.",
        "proviruses": "Proviral sequences.",
        "plasmid": "Plasmid sequences.",
        "virus_summary": "Virus classification summary.",
    },
    name="Identify and classify viral genomes",
    description="Perform comprehensive viral genome analysis to identify and "
    "classify viral, proviral, and plasmid sequences.",
    citations=[citations["geNomad"]],
)

importlib.import_module("q2_viromics.types._transformer")
