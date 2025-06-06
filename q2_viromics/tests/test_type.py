# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.types import CheckVDB, GenomadDB, ViromicsMetadata, Virsorter2Db


class TestCheckVDbType(TestPluginBase):
    package = "q2_viromics.tests"

    def test_CheckVDb_registration(self):
        self.assertRegisteredSemanticType(CheckVDB)


class TestGenomadDBType(TestPluginBase):
    package = "q2_viromics.tests"

    def test_GenomadDB_registration(self):
        self.assertRegisteredSemanticType(GenomadDB)


class TestViromicsMetadataType(TestPluginBase):
    package = "q2_viromics.tests"

    def test_ViromicsMetadata_registration(self):
        self.assertRegisteredSemanticType(ViromicsMetadata)


class TestVirsorter2DbType(TestPluginBase):
    package = "q2_viromics.virsorter2.tests"

    def test_Virsorter2Db_registration(self):
        self.assertRegisteredSemanticType(Virsorter2Db)