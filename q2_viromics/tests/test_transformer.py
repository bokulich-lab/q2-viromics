# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest

import pandas as pd
import qiime2
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.types._format import ViromicsMetadataDirFmt
from q2_viromics.types._transformer import combine_sample_metadata


class test_Viromics_to_qiime_metadata_transformer(TestPluginBase):
    package = "q2_viromics.tests"

    def test_ViromicsMetadataDirFmt_to_Metadata_transformer(self):
        transformer = self.get_transformer(ViromicsMetadataDirFmt, qiime2.Metadata)
        viromics_metadata = ViromicsMetadataDirFmt(
            self.get_data_path("viromics_metadata/viromics_metadata_dir"), "r"
        )
        metadata_obt = transformer(viromics_metadata)
        self.assertIsInstance(metadata_obt, qiime2.Metadata)

    def test_combine_sample_metadata(self):
        exp = pd.read_csv(
            self.get_data_path("viromics_metadata/combined.tsv"), sep="\t", index_col=0
        )
        exp.index.name = "id"
        exp.index = exp.index.astype(str)

        viromics_metadata = combine_sample_metadata(
            self.get_data_path("viromics_metadata/viromics_metadata_dir"),
        )

        pd.testing.assert_frame_equal(exp, viromics_metadata)


if __name__ == "__main__":
    unittest.main()
