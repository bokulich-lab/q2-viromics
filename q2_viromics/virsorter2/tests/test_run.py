# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import subprocess
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
import qiime2

from q2_viromics.virsorter2.analysis import virsorter2_run, vs2_run_execution


class TestVirsorter2Run(unittest.TestCase):
    @patch("q2_viromics.virsorter2.analysis.run_command")
    @patch("q2_viromics.virsorter2.analysis.DNAFASTAFormat")
    @patch("q2_viromics.virsorter2.analysis.Virsorter2DbDirFmt")
    def test_vs2_run_execution_success(
        self, mock_Virsorter2DbDirFmt, mock_DNAFASTAFormat, mock_run_command
    ):
        # Mock the paths
        mock_tmp = "/fake/tmp"
        mock_sequences = MagicMock()
        mock_sequences.path = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"

        # Call the function
        vs2_run_execution(
            mock_tmp,
            mock_sequences,
            mock_database,
            n_jobs=5,
            min_score=0.5,
            min_length=0,
        )

        # Expected command
        expected_cmd = [
            "virsorter",
            "run",
            "-w",
            mock_tmp,
            "-d",
            mock_database.path,
            "-i",
            mock_sequences.path,
            "-j",
            "5",
            "--min-score",
            "0.5",
            "--min-length",
            "0",
            "--use-conda-off",
        ]

        # Assert the command was called
        mock_run_command.assert_called_once_with(expected_cmd)

    @patch(
        "q2_viromics.virsorter2.analysis.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    def test_vs2_run_execution_failure(self, mock_run_command):
        # Mock the paths
        mock_tmp = "/fake/tmp"
        mock_sequences = MagicMock()
        mock_sequences.path = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"

        # Call the function and assert it raises an Exception
        with self.assertRaises(Exception) as context:
            vs2_run_execution(
                mock_tmp,
                mock_sequences,
                mock_database,
                n_jobs=5,
                min_score=0.5,
                min_length=0,
            )

        self.assertTrue(
            "An error was encountered while running virsorter2 run"
            in str(context.exception)
        )

    @patch("q2_viromics.virsorter2.analysis.vs2_run_execution")
    @patch("q2_viromics.virsorter2.analysis.DNAFASTAFormat")
    @patch("q2_viromics.virsorter2.analysis.pd.read_csv")
    @patch("shutil.copy")
    @patch("tempfile.TemporaryDirectory")
    def test_run_success(
        self,
        mock_tempdir,
        mock_shutil_copy,
        mock_read_csv,
        mock_DNAFASTAFormat,
        mock_vs2_run_execution,
    ):
        # Mock the context managers
        mock_tempdir.return_value.__enter__.return_value = "/fake/tmp"

        # Mock the data frames with string indices
        mock_viral_score_df = pd.DataFrame({"mock": ["data"]}, index=["sample_1"])
        mock_viral_boundary_df = pd.DataFrame({"mock": ["data"]}, index=["sample_2"])
        mock_read_csv.side_effect = [mock_viral_score_df, mock_viral_boundary_df]

        # Mock the sequences and database
        mock_sequences = MagicMock()
        mock_sequences.path = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"

        # Call the function
        result = virsorter2_run(
            mock_sequences, mock_database, n_jobs=5, min_score=0.5, min_length=0
        )

        # Assertions
        mock_vs2_run_execution.assert_called_once_with(
            "/fake/tmp", mock_sequences, mock_database, 5, 0.5, 0
        )
        mock_shutil_copy.assert_called_once_with(
            "/fake/tmp/final-viral-combined.fa", str(result[0])
        )
        mock_read_csv.assert_any_call(
            "/fake/tmp/final-viral-score.tsv", sep="\t", index_col=0
        )
        mock_read_csv.assert_any_call(
            "/fake/tmp/final-viral-boundary.tsv", sep="\t", index_col=0
        )

        # Convert the DataFrame to Metadata
        expected_viral_score_metadata = qiime2.Metadata(mock_viral_score_df)
        expected_viral_boundary_metadata = qiime2.Metadata(mock_viral_boundary_df)

        # Verify the Metadata
        self.assertEqual(result[1], expected_viral_score_metadata)
        self.assertEqual(result[2], expected_viral_boundary_metadata)


if __name__ == "__main__":
    unittest.main()
