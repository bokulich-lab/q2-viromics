# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import subprocess

import pandas as pd
from pyhmmer.plan7 import HMMFile
from qiime2.core.exceptions import ValidationError
from qiime2.plugin import model


# Format for validating general TSV files
class GeneralTSVFormat(model.TextFileFormat):
    def _validate_(self, level):
        try:
            # Read the TSV file into a DataFrame, ensuring it uses tab as a separator
            df = pd.read_csv(str(self), sep="\t", dtype=str, keep_default_na=False)

            # Ensure that the file is not empty
            if df.empty:
                raise ValidationError("The file is empty.")

            # Check if the DataFrame has more than one column
            # to ensure it's tab-separated
            if df.shape[1] < 2:
                raise ValidationError(
                    "The file does not appear to be a proper "
                    "TSV (tab-separated values) file."
                )

        except pd.errors.ParserError as e:
            raise ValidationError(f"File could not be parsed as TSV: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Validation error: {str(e)}")


class GeneralBinaryFileFormat(model.BinaryFileFormat):
    def _validate_(self, level):
        pass


# Format for validating HMM profiles files
class HMMFormat(model.TextFileFormat):
    def _validate_(self, level: str):
        tolerance = 0.0001
        with HMMFile(str(self)) as hmm_file:
            hmm = hmm_file.read()

            try:
                hmm.validate(tolerance=tolerance)
            except subprocess.CalledProcessError as e:
                raise ValidationError(
                    f"An error was encountered while validating hmm file, "
                    f"(return code {e.returncode})."
                )


# Directory format for the checkV Database
class CheckVDBDirFmt(model.DirectoryFormat):
    hmm_files = model.FileCollection(r"hmm_db/.+/.+\.hmm$", format=HMMFormat)
    readme = model.File(r"README.txt$", format=GeneralBinaryFileFormat)
    tsv_files_genome_db = model.FileCollection(
        r"genome_db/.+\.tsv$", format=GeneralTSVFormat
    )
    dmnd_files_genome_db = model.FileCollection(
        r"genome_db/.+\.dmnd$", format=GeneralBinaryFileFormat
    )
    faa_files_genome_db = model.FileCollection(
        r"genome_db/.+\.faa$", format=GeneralBinaryFileFormat
    )
    fna_files_genome_db = model.FileCollection(
        r"genome_db/.+\.fna$", format=GeneralBinaryFileFormat
    )
    log_files_genome_db = model.FileCollection(
        r"genome_db/.+\.log$", format=GeneralBinaryFileFormat
    )
    tsv_files_hmm_db = model.FileCollection(r"hmm_db/.+\.tsv$", format=GeneralTSVFormat)

    @hmm_files.set_path_maker
    def hmm_files_path_maker(self, dir, name):
        return "hmm/%s/%s.hmm" % dir, name

    @tsv_files_genome_db.set_path_maker
    def tsv_files_genome_db_path_maker(self, name):
        return "genome_db/%s.tsv" % name

    @dmnd_files_genome_db.set_path_maker
    def dmnd_files_genome_db_path_maker(self, name):
        return "genome_db/%s.dmnd" % name

    @faa_files_genome_db.set_path_maker
    def faa_files_genome_db_path_maker(self, name):
        return "genome_db/%s.faa" % name

    @fna_files_genome_db.set_path_maker
    def fna_files_genome_db_path_maker(self, name):
        return "genome_db/%s.fna" % name

    @log_files_genome_db.set_path_maker
    def log_files_genome_db_path_maker(self, name):
        return "genome_db/%s.log" % name

    @tsv_files_hmm_db.set_path_maker
    def tsv_files_hmm_db_path_maker(self, name):
        return "hmm_db/%s.tsv" % name
