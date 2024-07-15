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

from q2_viromics.checkv_fetch_db import checkv_download_database, checkv_fetch_db


class TestCheckVFetchDb(unittest.TestCase):
    @patch("q2_viromics.checkv_fetch_db.run_command")
    @patch("q2_viromics.checkv_fetch_db.CheckVDBDirFmt")
    def test_checkv_fetch_db_success(self, mock_CheckVDBDirFmt, mock_run_command):
        # Mock the CheckVDBDirFmt instance
        mock_database = MagicMock()
        mock_CheckVDBDirFmt.return_value = mock_database

        # Call the function
        result = checkv_fetch_db()

        # Check if checkv_download_database was called correctly
        expected_cmd = [
            "checkv",
            "download_database",
            str(mock_database),
        ]
        mock_run_command.assert_called_once_with(expected_cmd)

        # Check the return value
        self.assertEqual(result, mock_database)

    @patch(
        "q2_viromics.checkv_fetch_db.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    @patch("q2_viromics.checkv_fetch_db.CheckVDBDirFmt")
    def test_CheckV_fetch_db_failure(self, mock_CheckVDBDirFmt, mock_run_command):
        # Mock the CheckVDBDirFmt instance
        mock_database = MagicMock()
        mock_CheckVDBDirFmt.return_value = mock_database

        # Call the function and assert it raises an Exception
        with self.assertRaises(Exception) as context:
            checkv_fetch_db()

        self.assertTrue(
            "An error was encountered while running CheckV download_database"
            in str(context.exception)
        )

    @patch("q2_viromics.checkv_fetch_db.run_command")
    def test_vs2_setup_success(self, mock_run_command):
        # Mock the database path
        mock_database = MagicMock()
        mock_database.path = "/fake/path"

        # Call the function
        checkv_download_database(mock_database)

        # Expected command
        expected_cmd = [
            "checkv",
            "download_database",
            str(mock_database),
        ]

        # Assert the command was called
        mock_run_command.assert_called_once_with(expected_cmd)

    @patch(
        "q2_viromics.checkv_fetch_db.run_command",
        side_effect=subprocess.CalledProcessError(1, "cmd"),
    )
    def test_checkv_download_database_failure(self, mock_run_command):
        # Mock the database path
        mock_database = MagicMock()
        mock_database.path = "/fake/path"

        # Call the function and assert it raises an Exception
        with self.assertRaises(Exception) as context:
            checkv_download_database(mock_database)

        self.assertTrue(
            "An error was encountered while running CheckV download_database"
            in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
