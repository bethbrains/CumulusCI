import unittest
import os

import factory

from cumulusci.utils import temporary_dir
from cumulusci.tasks.bulkdata.tests.test_bulkdata import _make_task
from cumulusci.tasks.bulkdata.tests.dummy_data_factory import GenerateDummyData, Contact
from cumulusci.tasks.bulkdata import factory_utils


class TestFactoryUtils(unittest.TestCase):
    def test_factory(self):
        mapping_file = os.path.join(os.path.dirname(__file__), "mapping_v2.yml")

        with temporary_dir() as d:
            tmp_db_path = os.path.join(d, "temp.db")
            dburl = "sqlite:///" + tmp_db_path
            task = _make_task(
                GenerateDummyData,
                {
                    "options": {
                        "num_records": 10,
                        "mapping": mapping_file,
                        "database_url": dburl,
                    }
                },
            )
            task()


class TestAdder(unittest.TestCase):
    def test_adder(self):
        a = factory_utils.Adder(10)
        b = a(20)
        assert b == 30
        c = a(0)
        assert c == 30
        d = a(-5)
        assert d == 25
        a.reset(3)
        assert a(0) == 3


class TestFactories(unittest.TestCase):
    def test_factories(self):
        class Broken(factory.alchemy.SQLAlchemyModelFactory):
            class Meta:
                model = "xyzzy"

        with self.assertRaises(KeyError):
            factory_utils.Factories(None, {}, {"A": Contact, "B": Broken})
