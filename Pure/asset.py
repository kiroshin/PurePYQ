#  asset.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import os

__all__ = ['Asset']
_BASE_DIR = os.path.dirname(__file__)
_ASSETS_PATH = os.path.join(_BASE_DIR, "assets")


class Asset:
    class Icon:
        app = os.path.join(_ASSETS_PATH, "appicon.svg")
        fav = os.path.join(_ASSETS_PATH, "material_favorite_24dp_wght400.svg")
        fav_fill = os.path.join(_ASSETS_PATH, "material_favorite_24dp_wght400_fill.svg")

    class Script:
        schema = os.path.join(_ASSETS_PATH, "schema.sql")
