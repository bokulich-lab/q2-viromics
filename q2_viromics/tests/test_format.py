# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest
from unittest.mock import patch

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


class TestCheckVDBDirFmtPathMakers(unittest.TestCase):
    package = "q2_viromics.tests"

    def setUp(self):
        self.format = CheckVDBDirFmt("/dummy/path", mode="r")

    @patch.object(CheckVDBDirFmt, "hmm_files_path_maker")
    def test_hmm_files_path_maker(self, mock_hmm_files):
        mock_hmm_files.return_value = "/dummy/path/hmm/dir/name.hmm"
        result = self.format.hmm_files_path_maker("outer", "dir", "name")
        mock_hmm_files.assert_called_once_with("outer", "dir", "name")
        self.assertEqual(result, "/dummy/path/hmm/dir/name.hmm")

    @patch.object(CheckVDBDirFmt, "tsv_files_genome_db_path_maker")
    def test_tsv_files_genome_db_path_maker(self, mock_tsv_files):
        mock_tsv_files.return_value = "/dummy/path/genome_db/name.tsv"
        result = self.format.tsv_files_genome_db_path_maker("outer", "name")
        mock_tsv_files.assert_called_once_with("outer", "name")
        self.assertEqual(result, "/dummy/path/genome_db/name.tsv")

    @patch.object(CheckVDBDirFmt, "dmnd_files_genome_db_path_maker")
    def test_dmnd_files_genome_db_path_maker(self, mock_dmnd_files):
        mock_dmnd_files.return_value = "/dummy/path/genome_db/name.dmnd"
        result = self.format.dmnd_files_genome_db_path_maker("outer", "name")
        mock_dmnd_files.assert_called_once_with("outer", "name")
        self.assertEqual(result, "/dummy/path/genome_db/name.dmnd")

    @patch.object(CheckVDBDirFmt, "faa_files_genome_db_path_maker")
    def test_faa_files_genome_db_path_maker(self, mock_faa_files):
        mock_faa_files.return_value = "/dummy/path/genome_db/name.faa"
        result = self.format.faa_files_genome_db_path_maker("outer", "name")
        mock_faa_files.assert_called_once_with("outer", "name")
        self.assertEqual(result, "/dummy/path/genome_db/name.faa")

    @patch.object(CheckVDBDirFmt, "fna_files_genome_db_path_maker")
    def test_fna_files_genome_db_path_maker(self, mock_fna_files):
        mock_fna_files.return_value = "/dummy/path/genome_db/name.fna"
        result = self.format.fna_files_genome_db_path_maker("outer", "name")
        mock_fna_files.assert_called_once_with("outer", "name")
        self.assertEqual(result, "/dummy/path/genome_db/name.fna")

    @patch.object(CheckVDBDirFmt, "log_files_genome_db_path_maker")
    def test_log_files_genome_db_path_maker(self, mock_log_files):
        mock_log_files.return_value = "/dummy/path/genome_db/name.log"
        result = self.format.log_files_genome_db_path_maker("outer", "name")
        mock_log_files.assert_called_once_with("outer", "name")
        self.assertEqual(result, "/dummy/path/genome_db/name.log")

    @patch.object(CheckVDBDirFmt, "tsv_files_hmm_db_path_maker")
    def test_tsv_files_hmm_db_path_maker(self, mock_tsv_files):
        mock_tsv_files.return_value = "/dummy/path/hmm_db/name.tsv"
        result = self.format.tsv_files_hmm_db_path_maker("outer", "name")
        mock_tsv_files.assert_called_once_with("outer", "name")
        self.assertEqual(result, "/dummy/path/hmm_db/name.tsv")
