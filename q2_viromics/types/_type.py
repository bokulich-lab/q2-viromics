# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.sample_data import SampleData
from qiime2.plugin import SemanticType

CheckVDB = SemanticType("CheckVDB")
GenomadDB = SemanticType("GenomadDB")
ViromicsMetadata = SemanticType("ViromicsMetadata", variant_of=SampleData.field["type"])
Virsorter2Db = SemanticType("Virsorter2Db")
