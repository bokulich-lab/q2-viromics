# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------sss
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_viromics.virsorter2.types._format import (
    GeneralBinaryFileFormat,
    GeneralTSVFormat,
    HallmarkGeneListFormat,
    HMMFormat,
    RbsCatetoryFormat,
    RbsCatetoryNotesFormat,
    Virsorter2DbDirFmt,
)


class TestVirsorter2DbFormats(TestPluginBase):
    package = "q2_viromics.virsorter2.tests"

    def test_Virsorter2Db_GeneralTSVFormat(self):
        filepath = self.get_data_path("type/vs2_db/hmm/pfam/Pfam-A.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing element for a column in a random row
    def test_Virsorter2Db_GeneralTSVFormat_neg1(self):
        filepath = self.get_data_path("type/vs2_db_neg/Pfam-A-neg1.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "GeneralTSVFormat"):
            format.validate()

    # Test the case of an empty element for a column in a random row
    def test_Virsorter2Db_GeneralTSVFormat_neg2(self):
        filepath = self.get_data_path("type/vs2_db_neg/Pfam-A-neg2.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "GeneralTSVFormat"):
            format.validate()

    # Test the case of an empty file
    def test_Virsorter2Db_GeneralTSVFormat_neg3(self):
        filepath = self.get_data_path("type/vs2_db_neg/Pfam-A-neg3.tsv")
        format = GeneralTSVFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "GeneralTSVFormat"):
            format.validate()

    def test_Virsorter2Db_RbsCategoryNotesFormat(self):
        filepath = self.get_data_path("type/vs2_db/rbs/rbs-catetory-notes.tsv")
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing field
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg1(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-notes-neg1.tsv")
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    # Test the case of an empty element for the RBS field
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg2(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-notes-neg2.tsv")
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    # Test the case of an empty element for the Note field
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg3(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-notes-neg3.tsv")
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    # Empty file
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg4(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-notes-neg4.tsv")
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    # Only one column
    def test_Virsorter2Db_RbsCategoryNotesFormat_neg5(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-notes-neg5.tsv")
        format = RbsCatetoryNotesFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryNotesFormat"):
            format.validate()

    def test_Virsorter2Db_RbsCategoryFormat(self):
        filepath = self.get_data_path("type/vs2_db/rbs/rbs-catetory.tsv")
        format = RbsCatetoryFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing field
    def test_Virsorter2Db_RbsCategoryFormat_neg1(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-neg1.tsv")
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    # Test the case of an empty element for the RBS field
    def test_Virsorter2Db_RbsCategoryFormat_neg2(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-neg2.tsv")
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    # Test the case of an empty element for the catetory field
    def test_Virsorter2Db_RbsCategoryFormat_neg3(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-neg3.tsv")
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    # Empty file
    def test_Virsorter2Db_RbsCategoryFormat_neg4(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-neg4.tsv")
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    # missing column
    def test_Virsorter2Db_RbsCategoryFormat_neg5(self):
        filepath = self.get_data_path("type/vs2_db_neg/rbs-catetory-neg5.tsv")
        format = RbsCatetoryFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "RbsCatetoryFormat"):
            format.validate()

    def test_Virsorter2Db_HallmarkGeneListFormat(self):
        filepath = self.get_data_path("type/vs2_db/group/dsDNAphage/hallmark-gene.list")
        format = HallmarkGeneListFormat(filepath, mode="r")
        format.validate()

    # Test the case of a missing field
    def test_Virsorter2Db_HallmarkGeneListFormat_neg1(self):
        filepath = self.get_data_path("type/vs2_db_neg/hallmark-gene-neg1.list")
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    # Test the case of an empty element for the Gene field
    def test_Virsorter2Db_HallmarkGeneListFormat_neg2(self):
        filepath = self.get_data_path("type/vs2_db_neg/hallmark-gene-neg2.list")
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    # Test the case of an empty element for the Gene Description field
    def test_Virsorter2Db_HallmarkGeneListFormat_neg3(self):
        filepath = self.get_data_path("type/vs2_db_neg/hallmark-gene-neg3.list")
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    # Empty file
    def test_Virsorter2Db_HallmarkGeneListFormat_neg4(self):
        filepath = self.get_data_path("type/vs2_db_neg/hallmark-gene-neg4.list")
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    # Missing column
    def test_Virsorter2Db_HallmarkGeneListFormat_neg5(self):
        filepath = self.get_data_path("type/vs2_db_neg/hallmark-gene-neg5.list")
        format = HallmarkGeneListFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValidationError, "HallmarkGeneListFormat"):
            format.validate()

    def test_GeneralBinaryFileFormat(self):
        filepath = self.get_data_path("type/vs2_db/group/dsDNAphage/model")
        format = GeneralBinaryFileFormat(filepath, mode="r")
        format.validate()

    def test_HMMFormat(self):
        filepath = self.get_data_path("type/vs2_db/hmm/pfam/Pfam-A.hmm")
        format = HMMFormat(filepath, mode="r")
        format.validate()

    # Test missing mandatory field (LENG)
    def test_HMMFormat_neg1(self):
        filepath = self.get_data_path("type/vs2_db_neg/HMM-neg1.hmm")
        format = HMMFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            format.validate()

    # Test missing value (for MM)
    def test_HMMFormat_neg2(self):
        filepath = self.get_data_path("type/vs2_db_neg/HMM-neg2.hmm")
        format = HMMFormat(filepath, mode="r")
        with self.assertRaisesRegex(ValueError, "Invalid"):
            format.validate()

    def test_Virsorter2DbDirFmt(self):
        filepath = self.get_data_path("type/vs2_db/")
        format = Virsorter2DbDirFmt(filepath, mode="r")
        format.validate()
