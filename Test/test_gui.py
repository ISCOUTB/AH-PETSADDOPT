import unittest
from gui import show_client_options, show_admin_login

class TestGUI(unittest.TestCase):
    def test_admin_login_button(self):
        # Verifica si `show_admin_login` ejecuta sin errores
        try:
            show_admin_login()
        except Exception as e:
            self.fail(f"show_admin_login lanzó una excepción: {e}")

    def test_client_options(self):
        try:
            show_client_options()
        except Exception as e:
            self.fail(f"show_client_options lanzó una excepción: {e}")
