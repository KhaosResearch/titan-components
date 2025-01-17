import shutil
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from drama.models.task import TaskResult
from drama.storage import LocalStorage

from drama_enbic2lab.catalog.air.extractFromTemplate import execute
from drama_enbic2lab.catalog.air.tests import RESOURCES
from drama_enbic2lab.model import ExcelDataset


class extractFromTemplateTestCase(unittest.TestCase):
    def setUp(self) -> None:
        task_id, task_name = "tests", "test_ExtractFromTemplate"

        storage = LocalStorage(bucket_name=task_id, folder_name=task_name)
        storage.setup()

        # copy file to task dir
        dataset = shutil.copy(Path(RESOURCES, "template_malaga.xlsx"), storage.local_dir)

        # mock process
        self.pcs = MagicMock(storage=storage)
        self.pcs.get_from_upstream = MagicMock(return_value={"TempFile": [{"resource": dataset}]})

    def test_integration(self):
        # execute func
        data = execute(pcs=self.pcs, summary_sheet="Resumen", data_columns="A:AQ", code="esmala")

        # assert output data is valid
        self.assertIs(type(data), TaskResult)

    def tearDown(self) -> None:
        self.pcs.storage.remove_local_dir()


if __name__ == "__main__":
    unittest.main()
