
from django.test import SimpleTestCase
from servers.singleton import AccessManager


class AccessManagerTest(SimpleTestCase):
    def test_same_instance(self):
        manager1 = AccessManager()
        manager2 = AccessManager()

        self.assertIs(manager1, manager2)
        self.assertEqual(id(manager1), id(manager2))

    def test_record_access(self):
        manager = AccessManager()
        message = "Тестовый запрос"

        manager.record_access(message)

        self.assertIn(message, manager.get_access_log())
