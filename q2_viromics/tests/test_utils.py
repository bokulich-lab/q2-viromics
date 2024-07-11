# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest
from unittest.mock import patch

from q2_viromics._utils import run_command


class TestRunCommand(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_command_with_verbose(self, mock_run):
        cmd = ["echo", "hello"]
        run_command(cmd, verbose=True)
        mock_run.assert_called_once_with(cmd, check=True)

    @patch("subprocess.run")
    def test_run_command_no_verbose(self, mock_run):
        cmd = ["echo", "hello"]
        run_command(cmd, verbose=False)
        mock_run.assert_called_once_with(cmd, check=True)
