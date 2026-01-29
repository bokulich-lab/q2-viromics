# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.virsorter2.types._type import Virsorter2Db


class TestVirsorter2DbType(TestPluginBase):
    package = "q2_viromics.virsorter2.tests"

    def test_Virsorter2Db_registration(self):
        self.assertRegisteredSemanticType(Virsorter2Db)
