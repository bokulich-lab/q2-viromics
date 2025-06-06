# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import subprocess
import unittest
from unittest.mock import MagicMock, patch

from q2_viromics.genomad.db import genomad_download_database, genomad_fetch_db


class TestGenomadFetchDb(unittest.TestCase):
    @patch("q2_viromics.genomad.db.run_command")
    @patch("q2_viromics.genomad.db.GenomadDBDirFmt")
    def test_genomad_fetch_db_success(self, mock_GenomadDBDirFmt, mock_run_command):
        # Mock the GenomadDBDirFmt instance
        mock_database = MagicMock()
        mock_GenomadDBDirFmt.return_value = mock_database

        # Mock os.path.isdir to simulate presence of .ipynb_checkpoints directory
        with patch("os.path.exists", return_value=True):
            with patch("shutil.rmtree") as mock_rmtree:
                # Call the function
                result = genomad_fetch_db()

                # Check if genomad_download_database was called correctly
                expected_cmd = [
                    "genomad",
                    "download-database",
                    str(mock_database),
                ]
                mock_run_command.assert_called_once_with(expected_cmd)

                # Check if .ipynb_checkpoints directory was removed
                mock_rmtree.assert_called_once_with(
                    os.path.join(str(mock_database), "genomad_db/.ipynb_checkpoints/")
                )

                # Check the return value
                self.assertEqual(result, mock_database)

    @patch(
        "q2_viromics.genomad.db.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    @patch("q2_viromics.genomad.db.GenomadDBDirFmt")
    def test_genomad_fetch_db_failure(self, mock_GenomadDBDirFmt, mock_run_command):
        # Mock the GenomadDBDirFmt instance
        mock_database = MagicMock()
        mock_GenomadDBDirFmt.return_value = mock_database

        # Call the function and assert it raises an Exception
        with self.assertRaises(Exception) as context:
            genomad_fetch_db()

        self.assertTrue(
            "An error was encountered while running geNomad download-database"
            in str(context.exception)
        )

    @patch("q2_viromics.genomad.db.run_command")
    def test_genomad_download_database_success(self, mock_run_command):
        # Mock the database path
        mock_database = MagicMock()
        mock_database.path = "/fake/path"

        # Call the function
        genomad_download_database(mock_database)

        # Expected command
        expected_cmd = [
            "genomad",
            "download-database",
            str(mock_database),
        ]

        # Assert the command was called
        mock_run_command.assert_called_once_with(expected_cmd)


if __name__ == "__main__":
    unittest.main()
