#  style.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

_HEX_ATENEO_BLUE = "#003A6B"
_HEX_SAPPHIRE_BLUE = "#1B5886"
_HEX_QUEEN_BLUE = "#3776A1"
_HEX_LAKE_BLUE = "#5293BB"
_HEX_ICEBERG_BLUE = "#6EB1D6"
_HEX_BABY_BLUE = "#89CFF1"
_HEX_BLACK = "#000000"
_HEX_WHITE = "#FFFFFF"


class Style:
    class Color:
        Accent = _HEX_QUEEN_BLUE
        LightOnTitle = _HEX_BLACK
        LightOnText = _HEX_ATENEO_BLUE
        DarkOnTitle = _HEX_WHITE
        DarkOnText = _HEX_BABY_BLUE
        LightBack = _HEX_WHITE
        DarkBack = _HEX_ATENEO_BLUE
        TailBack = "#f5fafc"

    class Layout:
        SidebarMinWidth = 250
        SidebarMaxWidth = 300
        CellLineHeight = 28
        ColumnMinWidth = 150
        BarLineHeight = CellLineHeight * 2

    class Font:
        TextSize = 14

    class Space:
        Tiny = 8
        Narrow = 16
        Medium = 32
        Large = 64
