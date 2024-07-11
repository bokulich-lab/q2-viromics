# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.types._format import (
    CheckVDBDirFmt,
    GeneralBinaryFileFormat,
    GeneralTSVFormat,
    HMMFormat,
)


class TestCheckVDBFormats(TestPluginBase):
    package = "q2_viromics.tests"

    def test_CheckVDB_GeneralTSVFormat(self):
        filepath = self.get_data_path("type/checkVdb/genome_db/checkv_error.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing element for a column in a random row
    def test_CheckVDB_GeneralTSVFormat_neg1(self):
        filepath = self.get_data_path("type/negative/tsv_neg1.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "GeneralTSVFormat"):
            format.validate()

    # Test the case of an empty element for a column in a random row
    def test_CheckVDB_GeneralTSVFormat_neg2(self):
        filepath = self.get_data_path("type/negative/tsv_neg2.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "GeneralTSVFormat"):
            format.validate()

    def test_GeneralBinaryFileFormat(self):
        filepath = self.get_data_path("type/checkVdb/genome_db/checkv_reps.dmnd")
        format = GeneralBinaryFileFormat(filepath, mode="r")
        format.validate()

    def test_HMMFormat(self):
        filepath = self.get_data_path("type/checkVdb/hmm_db/checkv_hmms/1.hmm")
        format = HMMFormat(filepath, mode="r")
        format.validate()

    # Test missing mandatory field (LENG)
    def test_HMMFormat_neg1(self):
        filepath = self.get_data_path("type/negative/hmm_neg.hmm")
        format = HMMFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            format.validate()

    def test_CheckVDBDirFmt(self):
        filepath = self.get_data_path("type/checkVdb/")
        format = CheckVDBDirFmt(filepath, mode="r")
        format.validate()
