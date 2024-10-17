# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

import pandas as pd
import qiime2

from ..plugin_setup import plugin
from ._format import ViromicsMetadataDirFmt


def combine_sample_metadata(data_path):
    df_list = []

    # need to sort the contents of the data path
    # to ensure consistency between operating systems
    for file_name in sorted(os.listdir(str(data_path))):
        file_path = os.path.join(str(data_path), file_name)
        # Read the file into a DataFrame
        df = pd.read_csv(file_path, sep="\t")
        # Extract the sample name before the first underscore
        sample_name = file_name.split("_")[0]
        # Insert the sample name as a new column
        df.insert(0, "sample_id", sample_name)
        # Add the DataFrame to the list
        df_list.append(df)

    # Combine all DataFrames into one
    combined_df = pd.concat(df_list, ignore_index=True)

    # Ensure that the index is in correct format
    combined_df.index = combined_df.index.astype(str)
    combined_df.index.name = "id"

    # Return the combined DataFrame as a qiime2.Metadata object
    return combined_df


@plugin.register_transformer
def _1(data_path: ViromicsMetadataDirFmt) -> qiime2.Metadata:
    return qiime2.Metadata(combine_sample_metadata(data_path))
