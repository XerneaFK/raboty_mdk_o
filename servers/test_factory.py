
from django.test import SimpleTestCase
from servers.models import (
    AccessRequestFactory,
    ReadRequest,
    WriteRequest,
    AdminRequest,
)


class AccessRequestFactoryTest(SimpleTestCase):
    def test_create_read(self):
        obj = AccessRequestFactory.create(
            "read", "user1", "test_db"
        )
        self.assertIsInstance(obj, ReadRequest)

    def test_create_write(self):
        obj = AccessRequestFactory.create(
            "write", "user1", "test_db"
        )
        self.assertIsInstance(obj, WriteRequest)

    def test_create_admin(self):
        obj = AccessRequestFactory.create(
            "admin", "user1", "test_db"
        )
        self.assertIsInstance(obj, AdminRequest)

    def test_unknown_type(self):
        with self.assertRaises(ValueError):
            AccessRequestFactory.create(
                "unknown", "user1", "test_db"
            )
