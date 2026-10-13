"""Run with python -B tests/test_config.py; no external packages required."""
import importlib.util
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("render_config", ROOT / "scripts/render_config.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class ContextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.data = ""

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "agent-team-context":
            self.active = True

    def handle_data(self, data):
        if self.active:
            self.data += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.active = False


class ConfigTests(unittest.TestCase):
    def test_recommended_presets(self):
        presets = {p["id"]: p for p in renderer.presets()}
        self.assertEqual(list(presets), list("ABCDEFGH"))
        expected = {
            "B": [("gpt-6.1-sol", "high"), ("gpt-6-luna", "high")],
            "D": [("gpt-6-astra", "high"), ("gpt-6-luna", "high"), ("gpt-6.1-sol", "high")],
            "E": [("gpt-6-astra", "high"), ("gpt-6.1-sol", "high"), ("gpt-6-luna", "high")],
            "G": [("gpt-6.1-sol", "high"), ("gpt-6-luna", "high"), ("gpt-6-luna", "medium")],
            "H": [("gpt-6.1-sol", "high"), ("gpt-6-astra", "high"), ("gpt-6-luna", "high")],
        }
        for key, members in expected.items():
            self.assertEqual([(m["model"], m["effort"]) for m in presets[key]["members"]], members)
        for key in ("G", "H"):
            self.assertEqual(presets[key]["order"], "tested_review")

    def test_render_modes_preserve_context_and_escape_markup(self):
        context = {"capabilities": {"gpt-6-luna": ["medium", "high"]},
                   "max_concurrency": 2, "label": "</script><b>&"}
        parsed = []
        with tempfile.TemporaryDirectory() as directory:
            for mode in ("inline", "browser"):
                output = Path(directory) / (mode + ".html")
                renderer.render(context, output, mode)
                html = output.read_text(encoding="utf-8")
                self.assertEqual(html.startswith("<!doctype html>"), mode == "browser")
                parser = ContextParser()
                parser.feed(html)
                data = json.loads(parser.data)
                self.assertEqual(data.pop("presentation_mode"), mode)
                self.assertEqual(data["label"], context["label"])
                parsed.append(data)
        self.assertEqual(parsed[0], parsed[1])


if __name__ == "__main__":
    unittest.main()
