from pyfiglet import Figlet
from pygamelib.gfx import core
import sys
import os
import json

readme_tmpl = """
# figlet-$font_name

This font is automatically generated from the FIGlet font **$font_name**.

# comment

$figfontcomment

# credits

FIGlet is available at [http://www.figlet.org/](http://www.figlet.org/)

The fonts are from the [FIGlet font database](http://www.figlet.org/fontdb.cgi).

Each font is the property of its respective author. This is just an adaptation to the
pygamelib font format.
"""

config = {
    "scalable": False,
    "monospace": False,
    "colorable": True,
    "height": 11,
    "horizontal_spacing": 0,
    "vertical_spacing": 0,
    "fg_color": {"red": 255, "green": 255, "blue": 255},
    "bg_color": None,
    "glyphs_map": {},
}

font_name = "univers"
if len(sys.argv) > 1:
    font_name = sys.argv[1]

print(f"Loading font: {font_name}...", end="")
fl = Figlet(font=font_name)
print("done")
config["height"] = fl.Font.height
readme_tmpl = readme_tmpl.replace("$font_name", font_name)
readme_tmpl = readme_tmpl.replace("$figfontcomment", fl.Font.comment)

fc = core.SpriteCollection()

white = core.Color(255, 255, 255)

print("Generating sprites...", end="")
for char in fl.Font.chars:
    spr = None
    if chr(char) == " ":
        if fl.Font.width[char] <= fl.Font.width[ord("a")]:
            # This just doesn't work for our font system, so we create a bigger
            # space.
            spr = core.Sprite(
                size=[fl.Font.width[ord("a")], fl.Font.height],
                default_sprixel=core.Sprixel(" "),
                name=" ",
            )
    if spr is None:
        spr = core.Sprite(
            size=[fl.Font.width[char], fl.Font.height],
            default_sprixel=core.Sprixel(" "),
        )
        row = 0
        for line in fl.Font.chars[char]:
            col = 0
            for ch in line:
                if ch == fl.Font.hardBlank:
                    spr.set_sprixel(row, col, core.Sprixel(" ", fg_color=white))
                else:
                    spr.set_sprixel(row, col, core.Sprixel(ch, fg_color=white))
                col += 1
            row += 1
        spr.name = chr(char)
    fc.add(spr)
print("done")
print("Writting files...", end="")
os.makedirs(f"pygamelib/assets/fonts/figlet-{font_name}", exist_ok=True)
fc.to_json_file(f"pygamelib/assets/fonts/figlet-{font_name}/glyphs.spr")
with open(f"pygamelib/assets/fonts/figlet-{font_name}/config.json", "w") as file:
    json.dump(config, file)

with open(f"pygamelib/assets/fonts/figlet-{font_name}/Readme.md", "w") as file:
    file.write(readme_tmpl)

print("done")
