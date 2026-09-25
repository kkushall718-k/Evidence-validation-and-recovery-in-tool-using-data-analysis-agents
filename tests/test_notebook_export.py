"""Check that exporting saved notebook outputs does not modify the notebook."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NotebookExportTests(unittest.TestCase):
    def test_export_preserves_source_and_renders_saved_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "notebooks").mkdir()
            script = root / "scripts/export_notebook_html.py"
            shutil.copyfile(ROOT / "scripts/export_notebook_html.py", script)
            notebook = root / "notebooks/Thesis_Experiment_Reproduction.ipynb"
            original = json.dumps(
                {
                    "cells": [
                        {
                            "cell_type": "markdown",
                            "source": [
                                "# Example\n\npreregistered-style frozen protocol"
                            ],
                        },
                        {
                            "cell_type": "code",
                            "source": ["raise RuntimeError('must not execute')"],
                            "execution_count": 1,
                            "outputs": [
                                {
                                    "output_type": "stream",
                                    "text": ["saved output <test>"],
                                }
                            ],
                        },
                    ]
                }
            ).encode()
            notebook.write_bytes(original)
            subprocess.run(
                [sys.executable, str(script)], check=True, capture_output=True
            )
            self.assertEqual(notebook.read_bytes(), original)
            preview = notebook.with_suffix(".html").read_text()
            self.assertIn("preregistered-style frozen protocol", preview)
            self.assertIn("saved output &lt;test&gt;", preview)
            self.assertIn("<h1>Example</h1>", preview)


if __name__ == "__main__":
    unittest.main()
