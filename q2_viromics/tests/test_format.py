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
    GenomadDBDirFmt,
    HMMFormat,
)


class TestCheckVDBFormats(TestPluginBase):
    package = "q2_viromics.tests"

    def test_CheckVDB_GeneralTSVFormat(self):
        filepath = self.get_data_path("type/db/checkVdb/genome_db/checkv_error.tsv")
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
        filepath = self.get_data_path("type/db/checkVdb/genome_db/checkv_reps.dmnd")
        format = GeneralBinaryFileFormat(filepath, mode="r")
        format.validate()

    def test_HMMFormat(self):
        filepath = self.get_data_path("type/db/checkVdb/hmm_db/checkv_hmms/1.hmm")
        format = HMMFormat(filepath, mode="r")
        format.validate()

    # Test missing mandatory field (LENG)
    def test_HMMFormat_neg1(self):
        filepath = self.get_data_path("type/negative/hmm_neg.hmm")
        format = HMMFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            format.validate()

    def test_CheckVDBDirFmt(self):
        filepath = self.get_data_path("type/db/")
        format = CheckVDBDirFmt(filepath, mode="r")
        format.validate()


class TestCheckVDBDirFmtPathMakers(TestPluginBase):
    package = "q2_viromics.tests"

    def test_hmm_files_path_maker(self):
        obj = CheckVDBDirFmt("type/db/", mode="r")
        result_path = obj.hmm_files_path_maker(
            outer_dir="checkVdb", dir="checkv_hmms", name="1"
        )
        expected_path = "type/db/checkVdb/hmm_db/checkv_hmms/1.hmm"
        self.assertEqual(str(result_path), expected_path)

    def test_tsv_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("type/db/", mode="r")
        result_path = obj.tsv_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_error"
        )
        expected_path = "type/db/checkVdb/genome_db/checkv_error.tsv"
        self.assertEqual(str(result_path), expected_path)

    def test_dmnd_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("type/db/", mode="r")
        result_path = obj.dmnd_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_reps"
        )
        expected_path = "type/db/checkVdb/genome_db/checkv_reps.dmnd"
        self.assertEqual(str(result_path), expected_path)

    def test_faa_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("type/db/", mode="r")
        result_path = obj.faa_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_reps"
        )
        expected_path = "type/db/checkVdb/genome_db/checkv_reps.faa"
        self.assertEqual(str(result_path), expected_path)

    def test_fna_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("type/db/", mode="r")
        result_path = obj.fna_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_reps"
        )
        expected_path = "type/db/checkVdb/genome_db/checkv_reps.fna"
        self.assertEqual(str(result_path), expected_path)

    def test_log_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("type/db/", mode="r")
        result_path = obj.log_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_reps"
        )
        expected_path = "type/db/checkVdb/genome_db/checkv_reps.log"
        self.assertEqual(str(result_path), expected_path)

    def test_tsv_files_hmm_db_path_maker(self):
        obj = CheckVDBDirFmt("type/db/", mode="r")
        result_path = obj.tsv_files_hmm_db_path_maker(
            outer_dir="checkVdb", name="genome_lengths"
        )
        expected_path = "type/db/checkVdb/hmm_db/genome_lengths.tsv"
        self.assertEqual(str(result_path), expected_path)


class TestGenomadDBDirFmt(TestPluginBase):
    package = "q2_viromics.tests"

    def test_CheckVDB_GeneralTSVFormat(self):
        filepath = self.get_data_path("type/genomad_db/")
        format = GenomadDBDirFmt(filepath, mode="r")
        format.validate()
