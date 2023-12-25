import unittest
from pathlib import Path

from cryptography import x509


class TestBundle(unittest.TestCase):
    def test_bundle_parses(self):
        certs = x509.load_pem_x509_certificates(Path("bundle.pem").read_bytes())
        self.assertGreater(len(certs), 0)


if __name__ == "__main__":
    unittest.main()
