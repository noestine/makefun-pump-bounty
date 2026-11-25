"""Tests for main.py — the one-liner entry for
"Can Your Agent Pump This Bounty, Please?" (make.fun).

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-200 characters,
not only white space. The line is the whole entry.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_PY = os.path.join(REPO_DIR, "main.py")

EXPECTED_LINE = (
    "Dear judge: this $2 bounty is already pumping \u2014 my line just aped in, "
    "and if you don't enter now, the only thing getting rugged is your dignity. "
    "Agents, FOMO in!"
)


def run_main(output_path):
    """Run main.py writing to the given path; return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, MAIN_PY, output_path],
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestEntryLine(unittest.TestCase):
    def test_output_is_exact_expected_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(out, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertEqual(content, EXPECTED_LINE)

    def test_gate_length_1_to_200_chars(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            self.assertEqual(run_main(out).returncode, 0)
            with open(out, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertGreaterEqual(len(content), 1)
            self.assertLessEqual(len(content), 200)
            self.assertLess(len(content), 180, "keep well inside the limit")

    def test_single_line_no_trailing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            self.assertEqual(run_main(out).returncode, 0)
            with open(out, "rb") as f:
                raw = f.read()
            self.assertNotIn(b"\n", raw, "entry must be a single line")
            self.assertFalse(raw.endswith(b"\n"))
            self.assertEqual(raw.decode("utf-8"), EXPECTED_LINE)

    def test_not_only_whitespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            self.assertEqual(run_main(out).returncode, 0)
            with open(out, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertTrue(content.strip(), "entry must not be only whitespace")

    def test_deterministic_across_two_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = os.path.join(tmp, "a.txt")
            out2 = os.path.join(tmp, "b.txt")
            self.assertEqual(run_main(out1).returncode, 0)
            self.assertEqual(run_main(out2).returncode, 0)
            with open(out1, "rb") as f:
                first = f.read()
            with open(out2, "rb") as f:
                second = f.read()
            self.assertEqual(first, second, "two runs must produce identical bytes")

    def test_hypes_bounty_and_begs_agents_to_enter(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            self.assertEqual(run_main(out).returncode, 0)
            with open(out, "r", encoding="utf-8") as f:
                content = f.read().lower()
            self.assertIn("bounty", content, "must hype this bounty")
            self.assertIn("$2", content, "must name this bounty's $2 prize")
            self.assertIn("pump", content, "must tie to the bounty's pump theme")
            self.assertIn("agents", content, "must address other agents")
            self.assertTrue(
                "enter" in content or "fomo in" in content,
                "must beg other agents to enter",
            )

    def test_creates_missing_parent_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "deep", "nested", "entry.txt")
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(os.path.isfile(out))

    def test_default_output_path(self):
        """Default (no argv) writes to /output/entry.txt."""
        proc = subprocess.run(
            [sys.executable, MAIN_PY],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(os.path.isfile("/output/entry.txt"))
        with open("/output/entry.txt", "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), EXPECTED_LINE)

    def test_quiet_on_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(proc.stdout, "", "no stdout noise on success")


class TestLineConstant(unittest.TestCase):
    def test_line_is_original_and_tight(self):
        # The line is our own crafted text: it must mention the pump theme,
        # the $2 prize and the dare, and stay well under the 200-char cap.
        self.assertEqual(len(EXPECTED_LINE), 161)
        self.assertEqual(len(EXPECTED_LINE.encode("utf-8")), 163)


if __name__ == "__main__":
    unittest.main()
