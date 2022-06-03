import os

from django.test import TestCase

from .fiware.fiware import FIWARE


class DatabaseTestCase(TestCase):
    """Test case class for the database connections"""

    def test_fiware(self):
        self.__connector = FIWARE(os.getenv("OCB_URL"))
