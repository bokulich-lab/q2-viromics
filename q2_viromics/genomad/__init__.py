# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from .db import genomad_fetch_db
from .analysis import genomad_run

__all__ = ["genomad_fetch_db", "genomad_run"]
