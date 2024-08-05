# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.types._type import CheckVDB, CheckVMetadata, GenomadDB


class TestCheckVDbType(TestPluginBase):
    package = "q2_viromics.tests"

    def test_CheckVDb_registration(self):
        self.assertRegisteredSemanticType(CheckVDB)


class TestGenomadDBType(TestPluginBase):
    package = "q2_viromics.tests"

    def test_GenomadDB_registration(self):
        self.assertRegisteredSemanticType(GenomadDB)


class TestCheckVMetadataType(TestPluginBase):
    package = "q2_viromics.tests"

    def test_CheckVMetadata_registration(self):
        self.assertRegisteredSemanticType(CheckVMetadata)
