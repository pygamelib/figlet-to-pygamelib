#!/usr/bin/env python3

from pyfiglet import Figlet
from pygamelib.gfx import core
from pygamelib import base, engine, constants
import os
import json
import argparse

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


parser = argparse.ArgumentParser(
    description="A tool to convert a Figlet font into a pygamelib sprite-based font. "
    "Please read https://github.com/arnauddupuis/pygamelib/wiki/Font-creation for more "
    "information."
)

parser.add_argument(
    "--scalable",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="Declare the font as scalable. You have to make sure that it is actually "
    "scalable.",
)

parser.add_argument(
    "--monospace",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="Declare the font as monospace. It means that all characters have the same "
    "width. In that case, the width of the font is the width of the widest character.",
)

# parser.add_argument(
#     "--colorable",
#     action=argparse.BooleanOptionalAction,
#     default=True,
#     help="Declare the font as colorable. This means that the font is created using 2 "
#     "colors (background and foreground) and that the Font class will be able to use"
#     " this to allow colorization of the font. Read: "
#     "https://github.com/arnauddupuis/pygamelib/wiki/Font-creation for more info.",
# )

parser.add_argument(
    "--output-directory",
    type=str,
    action="store",
    required=False,
    default="",
    help="Specify the output directory. If set, all files generated will be store in "
    "that directory. If not, files are going to be stored in the current directory. "
    "The entire directory structure will be created if it does not exist.",
)

parser.add_argument(
    "--name",
    type=str,
    action="store",
    required=False,
    default="",
    help="Specify the name of the generated font. By default, it is "
    "figlet-<font name>.",
)

parser.add_argument(
    "--space-width",
    type=int,
    action="store",
    required=False,
    default=0,
    help="Specify the space character width. Sometimes the one in the Figlet font does "
    "not work/look good for the game. You can define the width of the space character "
    "and test different values.",
)

parser.add_argument(
    "--horizontal-spacing",
    type=int,
    action="store",
    required=False,
    default=0,
    help="Specify the horizontal spacing between glyphs.",
)

parser.add_argument(
    "--vertical-spacing",
    type=int,
    action="store",
    required=False,
    default=0,
    help="Specify the vertical spacing between glyphs.",
)

parser.add_argument(
    "--preview",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Show a preview rendering of the freshly created font.",
)

parser.add_argument(
    "font_name", help="The name of the Figlet font to convert. Ex: univers"
)

args = parser.parse_args()

config = {
    "scalable": args.scalable,
    "monospace": False,
    "colorable": True,
    "height": 11,
    "horizontal_spacing": args.horizontal_spacing,
    "vertical_spacing": args.vertical_spacing,
    "fg_color": {"red": 255, "green": 255, "blue": 255},
    "bg_color": None,
    "glyphs_map": {"default": "#"},
}

font_name = args.font_name

output_dir = "."
if args.output_directory:
    output_dir = args.output_directory

generated_font_name = "figlet-" + font_name
if args.name:
    generated_font_name = args.name

print(f"Loading font: {font_name}...", end="")
fl = Figlet(font=font_name)
print("done")
config["height"] = fl.Font.height
readme_tmpl = readme_tmpl.replace("$font_name", font_name)
readme_tmpl = readme_tmpl.replace("$figfontcomment", fl.Font.comment)

maxwidth = 0
for wi in fl.Font.width:
    if fl.Font.width[wi] > maxwidth:
        maxwidth = fl.Font.width[wi]
space_desired_width = maxwidth
if args.space_width and args.space_width >= 0:
    space_desired_width = args.space_width
elif fl.Font.width[ord(" ")] <= fl.Font.width[ord("a")]:
    space_desired_width = fl.Font.width[ord("a")]

if args.monospace:
    config["monospace"] = True
    config["width"] = maxwidth
    space_desired_width = maxwidth

print(f"Space width: {space_desired_width}")

fc = core.SpriteCollection()

white = core.Color(255, 255, 255)

print("Generating sprites...", end="")
for char in fl.Font.chars:
    spr = None
    if chr(char) == " ":
        # The space character is special. We want to make sure that it looks good and
        # allow more customization to the user of that script.
        spr = core.Sprite(
            size=[space_desired_width, fl.Font.height],
            default_sprixel=core.Sprixel(" "),
            name=" ",
        )
    else:
        char_width = fl.Font.width[char]
        if args.monospace:
            char_width = config["width"]
        spr = core.Sprite(
            size=[char_width, fl.Font.height],
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
os.makedirs(f"{output_dir}/pygamelib/assets/fonts/{generated_font_name}", exist_ok=True)
fc.to_json_file(f"{output_dir}/pygamelib/assets/fonts/{generated_font_name}/glyphs.spr")
with open(
    f"{output_dir}/pygamelib/assets/fonts/{generated_font_name}/config.json", "w"
) as file:
    json.dump(config, file)

with open(
    f"{output_dir}/pygamelib/assets/fonts/{generated_font_name}/Readme.md", "w"
) as file:
    file.write(readme_tmpl)

with open(
    f"{output_dir}/pygamelib/assets/fonts/{generated_font_name}/__init__.py", "w"
) as file:
    file.write("")

print("done")

if args.preview:
    print("Here is a test of the font:")
    s = engine.Screen(height=config["height"] * 3 + 3 * config["vertical_spacing"] + 11)
    t = base.Text(
        f"Test of the:\n{generated_font_name}\nfont",
        font=core.Font(f"{generated_font_name}", [f"{output_dir}/pygamelib/assets/"]),
    )
    s.place(t, 0, 0)
    offset = config["height"] * 3 + 3 * config["vertical_spacing"] + 1
    s.place(
        base.Text(
            "Configuration values of the font:",
            core.Color(0, 255, 50),
            style=constants.UNDERLINE,
        ),
        offset,
        0,
    )
    offset += 1
    for key in [
        "scalable",
        "monospace",
        "colorable",
        "height",
        "horizontal_spacing",
        "vertical_spacing",
        "fg_color",
        "bg_color",
    ]:
        k = base.Text(f"{key}:", core.Color(0, 255, 255), style=constants.BOLD)
        s.place(k, offset, 0)
        s.place(f"{config[key]}", offset, k.length + 1)
        offset += 1
    k = base.Text("Space width:", core.Color(0, 255, 255), style=constants.BOLD)
    s.place(k, offset, 0)
    s.place(f"{space_desired_width}", offset, k.length + 1)
    s.update()
else:
    print(
        base.Text(
            "Configuration values of the font:",
            core.Color(0, 255, 50),
            style=constants.UNDERLINE,
        )
    )
    for key in [
        "scalable",
        "monospace",
        "colorable",
        "height",
        "horizontal_spacing",
        "vertical_spacing",
        "fg_color",
        "bg_color",
    ]:
        k = base.Text(f"{key}:", core.Color(0, 255, 255), style=constants.BOLD)
        print(f"{k}: {config[key]}")
