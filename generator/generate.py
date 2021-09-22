#!/usr/bin/env python3
import os
import shutil
import json
from dataclasses import dataclass
import random

CHR_START: int = 65
ALPH_COUNT: int = 26

GEN_DIR: str = os.path.join(os.path.dirname(__file__), 'gen-out')
IMG_DIR: str = os.path.join(GEN_DIR, 'images')
META_DIR: str = os.path.join(GEN_DIR, 'metadata')

TRAITS: [str] = [
    'Treacherous',
    'Fearful',
    'Dauntless',
    'Foolproof',
    'Indignant',
    'Indomitable',
    'Reflective',
    'Sorrowful',
    'Divine',
    'Ornate',
    'Instructive',
    'Presumptuous',
    'Frail',
    'Wrathful',
    'Elusive',
    'Hesitant',
    'Skittish',
    'Honest',
    'Selfless',
    'Guileful',
    'Determined',
    'Foolhardy',
    'Studious',
    'Feeble',
    'Daring',
    'Dim',
    'Forceful',
    'Gallant',
    'Insouciant',
    'Predictable',
    'Unhurried',
    'Childish',
    'Irascible',
    'Fatalistic',
    'Dull',
    'Rigid',
    'Tactless',
    'Vacuous',
    'Willful',
    'Libidinous',
]

FONT_FAMILY = [
    'serif',
    'sans-serif',
    'monospace',
]

# dumb easy weighting, 1/10 chance for italic
FONT_STYLE = [
    'normal',
    'normal',
    'normal',
    'normal',
    'normal',
    'normal',
    'normal',
    'normal',
    'normal',
    'italic',
]

COLORS = [
    [
        "#0D171F",
        "#2E4659",
        "#435D73",
        "#5E788C",
        "#7A95A7",
        "#99B0BF",
        "#B4C5D1",
        "#D0DDE4",
        "#F1F4F7",
    ],
    [
        "#0D2829",
        "#154237",
        "#235C44",
        "#317545",
        "#428F42",
        "#6EA84A",
        "#A3C255",
        "#CFDB72",
    ],
    [
        "#750D10",
        "#94241A",
        "#B34428",
        "#D16630",
        "#E68D3E",
        "#EDAC4A",
        "#F5CB53",
        "#FFEA63",
    ],
    [
        "#5C1E1C",
        "#78362A",
        "#915237",
        "#AD7044",
        "#C78C58",
        "#E0AB72",
        "#EBC48A",
        "#F5D9A6",
    ],
    [
        "#3F1A4D",
        "#6D2975",
        "#943989",
        "#B3508D",
        "#CC6B8A",
        "#E6948F",
        "#F5BAA9",
    ],
    [
        "#1D1652",
        "#212870",
        "#2C488F",
        "#3973AD",
        "#53ACCC",
        "#74CEDA",
        "#A5E2E6",
        "#CDF1F4",
    ]
]

BORDER = [
    "",
]


@dataclass
class Info:
    """Struct for token metadata"""
    token_id: int
    trait: str

    digit: int
    little: str
    big: str

    base_color: str
    text_color: str

    border_count: int

    font_family: str
    font_style: str

    def display_name(self) -> str:
        return f'{self.big}{self.little}-{self.digit}'


def gen(n: int):
    for tok_id in range(n):
        digit: int = tok_id % 10
        le: int = CHR_START + (tok_id // 10) % ALPH_COUNT
        be: int = CHR_START + (tok_id // 10 // ALPH_COUNT) % ALPH_COUNT
        color_set = random.choice(COLORS)
        color_base = random.randint(0, len(color_set) - 2)
        yield Info(
            tok_id,
            random.choice(TRAITS),
            digit,
            chr(le),
            chr(be),
            color_set[color_base],
            color_set[color_base+1],
            random.randint(1,3),
            random.choice(FONT_FAMILY),
            random.choice(FONT_STYLE)
        )


def gen_meta(i: Info, ipfs_hash: str):
    with open(os.path.join(META_DIR, f'{i.token_id}.json'), 'w') as meta:
        mt = {
            "name": i.display_name(),
            "image": f'ipfs://{ipfs_hash}/{i.token_id}.svg',
            "description": f'{i.display_name()} ({i.trait})',
            "attributes": [
                {
                    "display_type": "number",
                    "trait_type": "digit",
                    "value": i.digit,
                },
                {
                    "trait_type": "big-end",
                    "value": i.big,
                },
                {
                    "trait_type": "little-end",
                    "value": i.little,
                },
                {
                    "trait_type": "affect",
                    "value": i.trait,
                },
                {
                    "trait_type": "color",
                    "value": i.base_color,
                },
                {
                    "trait_type": "font",
                    "value": i.font_family,
                },
                {
                    "trait_type": "font-style",
                    "value": i.font_style,
                },
                {
                    "trait_type": "border-count",
                    "value": i.border_count,
                    "display_type": "number",
                },
            ],
        }
        meta.write(json.dumps(mt))


def gen_svg(i: Info):
    width = 350
    height = 200
    aspect = width / height

    with open(os.path.join(IMG_DIR, f'{i.token_id}.svg'), 'w') as svg:
        borders = []
        for b in range(i.border_count):
            gap = 5 + b
            borders.append(f'<rect x="{gap}%" y="{gap*aspect}%" width="{100 - gap * 2}%" height="{100  - gap * 2 * aspect}%" style="fill-opacity:0;stroke-width:1;stroke:{i.text_color};"/>')
        borders = '\n'.join(borders)

        xml = f"""
        <svg viewBox="0 0 {width} {height}" style="background-color: {i.base_color}" xmlns="http://www.w3.org/2000/svg">
            <style>
                .subtext {{ 
                    font: {i.font_style} 10px {i.font_family};
                    fill: {i.text_color};
                    }}
                .primary {{
                    font: {i.font_style} 24px {i.font_family}; 
                    fill: {i.text_color};
                    }}
            </style>
            {borders}
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" class="primary">
                {i.display_name()}
            </text>
            <text x="50%" y="55%" dominant-baseline="hanging" text-anchor="middle" class="subtext">
                ({i.trait})
            </text>
        </svg>
        """
        svg.write(xml)


def run():
    tokens = gen(ALPH_COUNT * ALPH_COUNT * 10)
    for t in tokens:
        gen_svg(t)
        gen_meta(t, "QmfBACXSU9C8bjVfMaAeuVETohueqBCCZCFTx78AkcepRV")


def init():
    random.seed(12345)
    shutil.rmtree(GEN_DIR, True)
    os.makedirs(IMG_DIR)
    os.makedirs(META_DIR)


if __name__ == "__main__":
    init()
    run()
