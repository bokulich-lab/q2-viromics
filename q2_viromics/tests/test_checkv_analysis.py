# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import subprocess
import unittest
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
from q2_types.feature_data import DNAFASTAFormat

from q2_viromics.checkv_analysis import (
    checkv_analysis,
    checkv_end_to_end,
    read_tsv_file,
)


class TestCheckvAnalysis(unittest.TestCase):
    @patch("q2_viromics.checkv_analysis.run_command")
    def test_checkv_end_to_end_success(self, mock_run_command):
        # Mock the paths
        mock_tmp = "/fake/tmp"
        mock_sequences = MagicMock()
        mock_sequences.__str__.return_value = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"
        mock_database_listdir = ["internal_db"]

        with patch("os.listdir", return_value=mock_database_listdir):
            # Call the function
            checkv_end_to_end(
                mock_tmp,
                mock_sequences,
                mock_database,
                num_threads=1,
            )

        # Expected command
        expected_cmd = [
            "checkv",
            "end_to_end",
            "/fake/sequences",
            mock_tmp,
            "-d",
            "/fake/database/internal_db",
            "-t",
            "1",
        ]

        # Assert the command was called
        mock_run_command.assert_called_once_with(expected_cmd)

    @patch(
        "q2_viromics.checkv_analysis.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    def test_checkv_end_to_end_failure(self, mock_run_command):
        # Mock the paths
        mock_tmp = "/fake/tmp"
        mock_sequences = MagicMock(spec=DNAFASTAFormat)
        mock_sequences.path = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"
        mock_database_listdir = ["internal_db"]

        with patch("os.listdir", return_value=mock_database_listdir):
            # Call the function and assert it raises an Exception
            with self.assertRaises(Exception) as context:
                checkv_end_to_end(
                    mock_tmp,
                    mock_sequences,
                    mock_database,
                    num_threads=1,
                )

            self.assertTrue(
                "An error was encountered while running checkv end_to_end"
                in str(context.exception)
            )

    @patch("q2_viromics.checkv_analysis.checkv_end_to_end")
    @patch("shutil.move")
    @patch("tempfile.TemporaryDirectory")
    def test_checkv_analysis_success(
        self,
        mock_tempdir,
        mock_shutil_move,
        mock_checkv_end_to_end,
    ):
        # Mock the temporary directory context manager
        mock_tempdir.return_value.__enter__.return_value = "/fake/tmp"

        # Mock the data frames with string indices
        mock_quality_summary_df = pd.DataFrame({"mock": ["data"]}, index=["sample_1"])
        mock_contamination_df = pd.DataFrame({"mock": ["data"]}, index=["sample_2"])
        mock_completeness_df = pd.DataFrame({"mock": ["data"]}, index=["sample_3"])
        mock_complete_genomes_df = pd.DataFrame({"mock": ["data"]}, index=["sample_4"])

        # Set valid index names for Qiime2 Metadata
        mock_quality_summary_df.index.name = "sample-id"
        mock_contamination_df.index.name = "sample-id"
        mock_completeness_df.index.name = "sample-id"
        mock_complete_genomes_df.index.name = "sample-id"

        # Mock the sequences and database
        mock_sequences = MagicMock()
        mock_sequences.sample_dict.return_value = {"sample_1": "/fake/sequences"}

        mock_database = MagicMock()

        # Call the function
        result = checkv_analysis(mock_sequences, mock_database, num_threads=1)

        # Assertions for checkv_end_to_end call
        mock_checkv_end_to_end.assert_called_once_with(
            "/fake/tmp", "/fake/sequences", mock_database, 1
        )

        # Assertions for file movements
        mock_shutil_move.assert_any_call(
            "/fake/tmp/viruses.fna", str(result[0]) + "/sample_1_contigs.fa"
        )
        mock_shutil_move.assert_any_call(
            "/fake/tmp/proviruses.fna", str(result[1]) + "/sample_1_contigs.fa"
        )
        mock_shutil_move.assert_any_call(
            "/fake/tmp/quality_summary.tsv",
            str(result[2]) + "/sample_1_quality_summary.tsv",
        )
        mock_shutil_move.assert_any_call(
            "/fake/tmp/contamination.tsv",
            str(result[3]) + "/sample_1_contamination.tsv",
        )
        mock_shutil_move.assert_any_call(
            "/fake/tmp/completeness.tsv", str(result[4]) + "/sample_1_completeness.tsv"
        )
        mock_shutil_move.assert_any_call(
            "/fake/tmp/complete_genomes.tsv",
            str(result[5]) + "/sample_1_complete_genomes.tsv",
        )


class TestReadTSVFile(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="sample_name\tcol1\tcol2\nsample1\t1\t2\nsample2\t3\t4\n",
    )
    def test_read_tsv_file(self, mock_file):
        # Set up
        file_name = "test.tsv"
        tmp = "/tmp"

        # Expected DataFrame
        expected_df = pd.DataFrame(
            {"col1": [1, 3], "col2": [2, 4]}, index=["sample1", "sample2"]
        )
        expected_df.index.name = "sample_name"

        # Call the function
        result_df = read_tsv_file(file_name, tmp)

        # Assert the DataFrame equality
        pd.testing.assert_frame_equal(result_df, expected_df)


if __name__ == "__main__":
    unittest.main()
