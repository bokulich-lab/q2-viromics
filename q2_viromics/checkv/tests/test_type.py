# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.checkv.types._type import CheckVDB, ViromicsMetadata


class TestCheckVDbType(TestPluginBase):
    package = "q2_viromics.tests"

    def test_CheckVDb_registration(self):
        self.assertRegisteredSemanticType(CheckVDB)


class TestViromicsMetadataType(TestPluginBase):
    package = "q2_viromics.tests"

    def test_ViromicsMetadata_registration(self):
        self.assertRegisteredSemanticType(ViromicsMetadata)
