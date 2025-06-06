# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.types import (
    CheckVDBDirFmt,
    GeneralBinaryFileFormat,
    GeneralTSVFormat,
    GenomadDBDirFmt,
    HMMFormat,
    ViromicsMetadataDirFmt,
    RbsCatetoryNotesFormat,
    RbsCatetoryFormat,
    HallmarkGeneListFormat,
    Virsorter2DbDirFmt,
)


class TestCheckVDBFormats(TestPluginBase):
    package = "q2_viromics.tests"

    def test_CheckVDB_GeneralTSVFormat(self):
        filepath = self.get_data_path(
            "checkv/type/db/checkVdb/genome_db/checkv_error.tsv"
        )
        format = GeneralTSVFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing element for a column in a random row
    def test_CheckVDB_GeneralTSVFormat_neg1(self):
        filepath = self.get_data_path("checkv/type/negative/tsv_neg1.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "GeneralTSVFormat"):
            format.validate()

    # Test the case of an empty element for a column in a random row
    def test_CheckVDB_GeneralTSVFormat_neg2(self):
        filepath = self.get_data_path("checkv/type/negative/tsv_neg2.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "GeneralTSVFormat"):
            format.validate()

    def test_GeneralBinaryFileFormat(self):
        filepath = self.get_data_path(
            "checkv/type/db/checkVdb/genome_db/checkv_reps.dmnd"
        )
        format = GeneralBinaryFileFormat(filepath, mode="r")
        format.validate()

    def test_HMMFormat(self):
        filepath = self.get_data_path(
            "checkv/type/db/checkVdb/hmm_db/checkv_hmms/1.hmm"
        )
        format = HMMFormat(filepath, mode="r")
        format.validate()

    # Test missing mandatory field (LENG)
    def test_HMMFormat_neg1(self):
        filepath = self.get_data_path("checkv/type/negative/hmm_neg.hmm")
        format = HMMFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            format.validate()

    def test_CheckVDBDirFmt(self):
        filepath = self.get_data_path("checkv/type/db/")
        format = CheckVDBDirFmt(filepath, mode="r")
        format.validate()


class TestCheckVDBDirFmtPathMakers(TestPluginBase):
    package = "q2_viromics.tests"

    def test_hmm_files_path_maker(self):
        obj = CheckVDBDirFmt("checkv/type/db/", mode="r")
        result_path = obj.hmm_files_path_maker(
            outer_dir="checkVdb", dir="checkv_hmms", name="1"
        )
        expected_path = "checkv/type/db/checkVdb/hmm_db/checkv_hmms/1.hmm"
        self.assertEqual(str(result_path), expected_path)

    def test_tsv_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("checkv/type/db/", mode="r")
        result_path = obj.tsv_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_error"
        )
        expected_path = "checkv/type/db/checkVdb/genome_db/checkv_error.tsv"
        self.assertEqual(str(result_path), expected_path)

    def test_dmnd_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("checkv/type/db/", mode="r")
        result_path = obj.dmnd_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_reps"
        )
        expected_path = "checkv/type/db/checkVdb/genome_db/checkv_reps.dmnd"
        self.assertEqual(str(result_path), expected_path)

    def test_faa_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("checkv/type/db/", mode="r")
        result_path = obj.faa_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_reps"
        )
        expected_path = "checkv/type/db/checkVdb/genome_db/checkv_reps.faa"
        self.assertEqual(str(result_path), expected_path)

    def test_fna_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("checkv/type/db/", mode="r")
        result_path = obj.fna_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_reps"
        )
        expected_path = "checkv/type/db/checkVdb/genome_db/checkv_reps.fna"
        self.assertEqual(str(result_path), expected_path)

    def test_log_files_genome_db_path_maker(self):
        obj = CheckVDBDirFmt("checkv/type/db/", mode="r")
        result_path = obj.log_files_genome_db_path_maker(
            outer_dir="checkVdb", name="checkv_reps"
        )
        expected_path = "checkv/type/db/checkVdb/genome_db/checkv_reps.log"
        self.assertEqual(str(result_path), expected_path)

    def test_tsv_files_hmm_db_path_maker(self):
        obj = CheckVDBDirFmt("checkv/type/db/", mode="r")
        result_path = obj.tsv_files_hmm_db_path_maker(
            outer_dir="checkVdb", name="genome_lengths"
        )
        expected_path = "checkv/type/db/checkVdb/hmm_db/genome_lengths.tsv"
        self.assertEqual(str(result_path), expected_path)


class TestGenomadDBDirFmt(TestPluginBase):
    package = "q2_viromics.tests"

    def test_GenomadDB_DirFmt(self):
        filepath = self.get_data_path("genomad/genomad_database_dir/")
        format = GenomadDBDirFmt(filepath, mode="r")
        format.validate()


class TestViromicsMetadataDirFmt(TestPluginBase):
    package = "q2_viromics.tests"

    def test_ViromicsMetadataDirFmt(self):
        filepath = self.get_data_path("checkv/type/checkVMetadata/")
        format = ViromicsMetadataDirFmt(filepath, mode="r")
        format.validate()

    def test_ViromicsMetadataDirFmt_path_maker(self):
        obj = ViromicsMetadataDirFmt("checkv/type/checkVMetadata/", mode="r")
        result_path = obj.metadata_files_path_maker(name="sample1_quality_summary")
        expected_path = "checkv/type/checkVMetadata/sample1_quality_summary.tsv"
        self.assertEqual(str(result_path), expected_path)


class TestVirsorter2DbFormats(TestPluginBase):
    package = "q2_viromics.tests"

    def test_Virsorter2Db_GeneralTSVFormat(self):
        filepath = self.get_data_path("virsorter2/type/vs2_db/hmm/pfam/Pfam-A.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        format.validate()

    # Test the case of an empty file
    def test_Virsorter2Db_GeneralTSVFormat_neg3(self):
        filepath = self.get_data_path("virsorter2/type/vs2_db_neg/Pfam-A-neg3.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "GeneralTSVFormat"):
            format.validate()

    def test_Virsorter2Db_RbsCategoryNotesFormat(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db/rbs/rbs-catetory-notes.tsv"
        )
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing field
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg1(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-notes-neg1.tsv"
        )
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    # Test the case of an empty element for the RBS field
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg2(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-notes-neg2.tsv"
        )
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    # Test the case of an empty element for the Note field
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg3(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-notes-neg3.tsv"
        )
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    # Empty file
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg4(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-notes-neg4.tsv"
        )
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    # Only one column
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg5(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-notes-neg5.tsv"
        )
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    def test_Virsorter2Db_RbsCategoryFormat(self):
        filepath = self.get_data_path("virsorter2/type/vs2_db/rbs/rbs-catetory.tsv")
        format = RbsCatetoryFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing field
    def test_Virsorter2Db_RbsCategoryFormat_neg1(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-neg1.tsv"
        )
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    # Test the case of an empty element for the RBS field
    def test_Virsorter2Db_RbsCategoryFormat_neg2(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-neg2.tsv"
        )
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    # Test the case of an empty element for the catetory field
    def test_Virsorter2Db_RbsCategoryFormat_neg3(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-neg3.tsv"
        )
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    # Empty file
    def test_Virsorter2Db_RbsCategoryFormat_neg4(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-neg4.tsv"
        )
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    # missing column
    def test_Virsorter2Db_RbsCategoryFormat_neg5(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/rbs-catetory-neg5.tsv"
        )
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    def test_Virsorter2Db_HallmarkGeneListFormat(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db/group/dsDNAphage/hallmark-gene.list"
        )
        format = HallmarkGeneListFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing field
    def test_Virsorter2Db_HallmarkGeneListFormat_neg1(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/hallmark-gene-neg1.list"
        )
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    # Test the case of an empty element for the Gene field
    def test_Virsorter2Db_HallmarkGeneListFormat_neg2(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/hallmark-gene-neg2.list"
        )
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    # Test the case of an empty element for the Gene Description field
    def test_Virsorter2Db_HallmarkGeneListFormat_neg3(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/hallmark-gene-neg3.list"
        )
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    # Empty file
    def test_Virsorter2Db_HallmarkGeneListFormat_neg4(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/hallmark-gene-neg4.list"
        )
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    # Missing column
    def test_Virsorter2Db_HallmarkGeneListFormat_neg5(self):
        filepath = self.get_data_path(
            "virsorter2/type/vs2_db_neg/hallmark-gene-neg5.list"
        )
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    def test_GeneralBinaryFileFormat(self):
        filepath = self.get_data_path("virsorter2/type/vs2_db/group/dsDNAphage/model")
        format = GeneralBinaryFileFormat(filepath, mode="r")
        format.validate()

    def test_HMMFormat(self):
        filepath = self.get_data_path("virsorter2/type/vs2_db/hmm/pfam/Pfam-A.hmm")
        format = HMMFormat(filepath, mode="r")
        format.validate()

    # Test missing mandatory field (LENG)
    def test_HMMFormat_neg1(self):
        filepath = self.get_data_path("virsorter2/type/vs2_db_neg/HMM-neg1.hmm")
        format = HMMFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            format.validate()

    # Test missing value (for MM)
    def test_HMMFormat_neg2(self):
        filepath = self.get_data_path("virsorter2/type/vs2_db_neg/HMM-neg2.hmm")
        format = HMMFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            format.validate()

    def test_Virsorter2DbDirFmt(self):
        filepath = self.get_data_path("virsorter2/type/vs2_db/")
        format = Virsorter2DbDirFmt(filepath, mode="r")
        format.validate()
