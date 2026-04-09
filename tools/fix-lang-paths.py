# -*- coding: utf-8 -*-
"""Fix ../ paths and lang switch in hu/*.html; fix lang switch in root *.html."""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HU = os.path.join(ROOT, "hu")

LANG_BLOCK_HU_OLD = """        <div class="lang-switch" aria-label="Nyelvválasztó">
          <a href="#" class="lang-switch__link" hreflang="de" lang="de">DE</a>
          <span class="lang-switch__sep" aria-hidden="true">|</span>
          <a href="#" class="lang-switch__link lang-switch__link--current" hreflang="hu" lang="hu" aria-current="true">HU</a>
        </div>"""


def fix_asset_paths(s: str) -> str:
    s = s.replace('href="css/', 'href="../css/')
    s = s.replace('src="js/', 'src="../js/')
    s = s.replace('src="assets/', 'src="../assets/')
    s = s.replace('href="assets/', 'href="../assets/')
    return s


def lang_block_hu_subdir(basename: str) -> str:
    return f"""        <div class="lang-switch" aria-label="Nyelvválasztó">
          <a href="../{basename}" class="lang-switch__link" hreflang="de" lang="de">DE</a>
          <span class="lang-switch__sep" aria-hidden="true">|</span>
          <a href="{basename}" class="lang-switch__link lang-switch__link--current" hreflang="hu" lang="hu" aria-current="true">HU</a>
        </div>"""


def lang_block_root_de(basename: str) -> str:
    return f"""        <div class="lang-switch" aria-label="Sprachauswahl">
          <a href="{basename}" class="lang-switch__link lang-switch__link--current" hreflang="de" lang="de" aria-current="true">DE</a>
          <span class="lang-switch__sep" aria-hidden="true">|</span>
          <a href="hu/{basename}" class="lang-switch__link" hreflang="hu" lang="hu">HU</a>
        </div>"""


def process_hu():
    for path in glob.glob(os.path.join(HU, "*.html")):
        bn = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            s = f.read()
        s = fix_asset_paths(s)
        if LANG_BLOCK_HU_OLD not in s:
            raise SystemExit(f"Expected lang block not found: {path}")
        s = s.replace(LANG_BLOCK_HU_OLD, lang_block_hu_subdir(bn), 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        print("hu OK", bn)


def process_root_lang_only():
    for path in glob.glob(os.path.join(ROOT, "*.html")):
        bn = os.path.basename(path)
        if bn.startswith("."):
            continue
        with open(path, "r", encoding="utf-8") as f:
            s = f.read()
        if LANG_BLOCK_HU_OLD not in s:
            print("skip (no block)", bn)
            continue
        s = s.replace(LANG_BLOCK_HU_OLD, lang_block_root_de(bn), 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        print("root lang OK", bn)


if __name__ == "__main__":
    process_hu()
    process_root_lang_only()
