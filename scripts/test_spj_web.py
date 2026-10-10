#!/usr/bin/env python3
"""Static safety and parity checks for the browser-only SPJ prototype."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class SPJWebTests(unittest.TestCase):
    def test_form_contract(self):
        html = (ROOT / "tools/kalkulator-pajak-spj.html").read_text(encoding="utf-8")
        for field in ('name="jenis"', 'name="tanggal" type="date" required',
                      'name="nilai"', 'name="rekanan"', 'name="dokumen"', 'name="metode"'):
            with self.subTest(field=field):
                self.assertIn(field, html)
        self.assertIn("noindex,nofollow", html)
        self.assertIn("BELUM SIAP", html)

    def test_browser_guardrails(self):
        js = (ROOT / "assets/spj-prototype.js").read_text(encoding="utf-8")
        for token in ("/^[0-9]+$/", "Number.isSafeInteger", "getUTCFullYear",
                      "KKPD", "Marketplace", "2026-10-01",
                      "PERLU VERIFIKASI", "replaceChildren"):
            with self.subTest(token=token):
                self.assertIn(token, js)
        for unsafe in ("innerHTML", "fetch(", "XMLHttpRequest", "eval("):
            self.assertNotIn(unsafe, js)

if __name__ == "__main__":
    unittest.main()
