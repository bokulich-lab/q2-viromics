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

from q2_viromics.genomad.analysis import genomad_run, genomad_end_to_end


class TestGenomadAnalysis(unittest.TestCase):
    @patch("q2_viromics.genomad.analysis.run_command")
    def test_genomad_end_to_end_success(self, mock_run_command):
        # Mock the paths
        mock_tmp = "/fake/tmp"
        mock_sequences = MagicMock()
        mock_sequences.__str__.return_value = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"
        mock_database_listdir = ["internal_db"]

        with patch("os.listdir", return_value=mock_database_listdir):
            # Call the function
            genomad_end_to_end(
                mock_tmp,
                mock_sequences,
                mock_database,
                num_threads=1,
                splits=0,
                min_score=0.7,
                min_number_genes=1,
                conservative_taxonomy=False,
            )

        # Expected command
        expected_cmd = [
            "genomad",
            "end-to-end",
            "--cleanup",
            "--splits",
            "0",
            "--min-score",
            "0.7",
            "--min-number-genes",
            "1",
            "--threads",
            "1",
            "--disable-nn-classification",
            "/fake/sequences",
            mock_tmp,
            "/fake/database/internal_db",
        ]

        # Assert the command was called
        mock_run_command.assert_called_once_with(expected_cmd)

    @patch(
        "q2_viromics.genomad.analysis.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    def test_genomad_end_to_end_failure(self, mock_run_command):
        # Mock the paths
        mock_tmp = "/fake/tmp"
        mock_sequences = MagicMock()
        mock_sequences.__str__.return_value = "/fake/sequences"
        mock_database = MagicMock()
        mock_database.path = "/fake/database"
        mock_database_listdir = ["internal_db"]

        with patch("os.listdir", return_value=mock_database_listdir):
            # Call the function and assert it raises an Exception
            with self.assertRaises(Exception) as context:
                genomad_end_to_end(
                    mock_tmp,
                    mock_sequences,
                    mock_database,
                    num_threads=1,
                    splits=0,
                    min_score=0.7,
                    min_number_genes=1,
                    conservative_taxonomy=False,
                )

            self.assertTrue(
                "An error was encountered while running genomad end-to-end"
                in str(context.exception)
            )

    @patch("q2_viromics.genomad.analysis.genomad_end_to_end")
    @patch("q2_viromics.genomad.analysis.ContigSequencesDirFmt")
    @patch("shutil.move")
    @patch("tempfile.TemporaryDirectory")
    @patch("os.path.exists", return_value=True)
    @patch("os.makedirs")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_genomad_analysis_success(
        self,
        mock_open,
        mock_makedirs,
        mock_path_exists,
        mock_tempdir,
        mock_shutil_move,
        mock_ContigSequencesDirFmt,
        mock_genomad_end_to_end,
    ):
        # Mock the context managers
        mock_tempdir.return_value.__enter__.return_value = "/fake/tmp"

        # Mock the ContigSequencesDirFmt instance and its methods
        mock_sequences = mock_ContigSequencesDirFmt.return_value
        mock_sequences.sample_dict.return_value = {"s1": "/fake/contigs.fa"}

        # Mock the database
        mock_database = MagicMock()
        mock_database.path = "/fake/database"

        # Call the function
        result = genomad_run(
            mock_sequences,
            mock_database,
            num_threads=1,
            splits=0,
            min_score=0.7,
            min_number_genes=1,
            conservative_taxonomy=False,
        )

        # Assertions
        mock_genomad_end_to_end.assert_called_once_with(
            "/fake/tmp", "/fake/contigs.fa", mock_database, 1, 0, 0.7, 1, False
        )

        # Expected paths
        expected_files_and_destinations = [
            (
                "/fake/tmp/s1_contigs_summary/s1_contigs_virus.fna",
                f"{str(result[0])}/s1_contigs.fa",
            ),
            (
                "/fake/tmp/s1_contigs_find_proviruses/s1_contigs_provirus.fna",
                f"{str(result[1])}/s1_contigs.fa",
            ),
            (
                "/fake/tmp/s1_contigs_summary/s1_contigs_plasmid.fna",
                f"{str(result[2])}/s1_contigs.fa",
            ),
            (
                "/fake/tmp/s1_contigs_summary/s1_contigs_virus_summary.tsv",
                f"{str(result[3])}/s1_virus_summary.tsv",
            ),
        ]

        # Assert if shutil.move was called correctly
        for src, dst in expected_files_and_destinations:
            mock_shutil_move.assert_any_call(src, dst)


if __name__ == "__main__":
    unittest.main()
