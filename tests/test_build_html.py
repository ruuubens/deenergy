import os
import subprocess
import tempfile
import unittest


class BuildHtmlTests(unittest.TestCase):
    def test_build_html_filters_cet_window(self):
        root = os.path.dirname(os.path.dirname(__file__))
        fixture = os.path.join(root, "tests", "fixtures", "api_sample.json")
        script = os.path.join(root, "scripts", "build_html.py")

        with tempfile.TemporaryDirectory() as tmp:
            output = os.path.join(tmp, "out.html")
            subprocess.check_call([
                "python3",
                script,
                "--input",
                fixture,
                "--output",
                output,
                "--postal-code",
                "80339",
                "--date",
                "2026-03-01"
            ])

            with open(output, "r", encoding="utf-8") as fh:
                html = fh.read()

        self.assertIn("08:00", html)
        self.assertIn("12:00", html)
        self.assertIn("23:00", html)
        self.assertNotIn("07:00", html)


if __name__ == "__main__":
    unittest.main()
