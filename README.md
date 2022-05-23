# figlet-to-pygamelib
A small script to automatically convert Figlet fonts to the Pygamelib's sprite format.

## Usage

The easy way:

                figlet-to-pygamelib.py <figlet font name>

The script accept some options:

 - -h, --help            show this help message and exit
 - --scalable, --no-scalable
                        Declare the font as scalable. You have to make sure that it is actually scalable. (default: False)
 - --monospace, --no-monospace
                        Declare the font as monospace. It means that all characters have the same width. In that case, the width of the font is the width of the widest
                        character. (default: False)
 - --output-directory OUTPUT_DIRECTORY
                        Specify the output directory. If set, all files generated will be store in that directory. If not, files are going to be stored in the current directory.
                        The entire directory structure will be created if it does not exist.
 - --space-width SPACE_WIDTH
                        Specify the space character width. Sometimes the one in the Figlet font does not work/look good for the game. You can define the width of the space
                        character and test different values.
 - --test, --no-test     Show a test rendering of the freshly created font. (default: False)