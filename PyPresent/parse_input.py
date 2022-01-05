"""read and parse the lines from the formatted text file"""

# standard library
from typing import Generator, List
from collections import OrderedDict

# text identifiers
TITLE = 'title:'
SUBTITLE = 'subtitle:'
SLIDE_TITLE = ('[', ']')
BULLET = '.'
PICTURE = 'picture:'
TEXT_TYPE = {TITLE: 'title', SUBTITLE: 'subtitle', SLIDE_TITLE[0]: 'title',
             BULLET: 'bullet', PICTURE: 'picture'}
# slide identifiers
TYPE_TITLE = 'title'
TYPE_TEXT = 'text'
TYPE_IMAGE = 'image'
SLIDE_TYPE = {'title': TYPE_TITLE, 'subtitle': TYPE_TITLE, 'bullet': TYPE_TEXT,
              'picture': TYPE_IMAGE}

def read_file(in_file: str) -> List[str]:
    """Return the text in the file
    :param in_file: str of the location to read from
    :return: str of the text in the file
    """
    try:
        with open(in_file, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        raise SystemExit(f'Error - file does not exist: {infile}')
    except Exception as other:
        raise SystemExit(f'Error - {other}')

def parse_lines(lines: str) -> List[list]:
    """Separate lines into slides with types (title, text, image)
    :param lines: input text
    :return: list of lists each representing a slide

    Title: Awesome Presentation
    Subtitle: by XYZ

    [slide one title]
    .bullet one
    .two

    .slide two bullet
    .some fact

    [title of slide three]
    picture: /some/path
    -> [[('title', 'Awesome Presentation'), ('subtitle', 'by XYZ'), 'title'],
        [('title', 'slide one title'), ('bullet', 'bullet one'), ('bullet', 'two'), 'text'],
        [('bullet', 'slide two bullet'), ('bullet', 'some fact'), 'text'],
        [('title, 'title of slide three'), ('picture', '/some/path'), 'image']]
    """
    slides = []
    current_slide = []
    for index, line in enumerate(lines, 1):
        if line.isspace():
            current_slide.append(SLIDE_TYPE.get(current_slide[-1][0]))
            slides.append(current_slide)
            current_slide = []
            continue

        line = line.strip()
        type_of_line = identify_line(line)
        if not type_of_line:
            print(f'Line {index} skipped')
            continue
        data = extract_data(line)
        current_slide.append((type_of_line, data))

    if current_slide:
        current_slide.append(SLIDE_TYPE.get(current_slide[-1][0]))
        slides.append(current_slide)
    return slides

def identify_line(line: str) -> str:
    """Identify if line is contained in IDS
    :param line: str to check type of
    :return: the type
    """
    l = line.lower()
    if l.startswith(TITLE):
        return TEXT_TYPE[TITLE]
    elif l.startswith(SUBTITLE):
        return TEXT_TYPE[SUBTITLE]
    elif l.startswith(SLIDE_TITLE[0]):
        return TEXT_TYPE[SLIDE_TITLE[0]]
    elif l.startswith(BULLET):
        return TEXT_TYPE[BULLET]
    elif l.startswith(PICTURE):
        return TEXT_TYPE[PICTURE]

def extract_data(line: str) -> str:
    """Extract only the required text from the data
    :param type_of_data: used to determine where to extract
    :param line: str to get data from
    :return: str of extracted data
    """
    l = line.lower()
    if l.startswith(TITLE) or l.startswith(SUBTITLE) or l.startswith(PICTURE):
        assert TITLE[-1] == SUBTITLE[-1] == PICTURE[-1], 'last character not consistent'
        return ''.join(line.split(TITLE[-1], 1)[1:]).strip()
    elif l.startswith(SLIDE_TITLE[0]):
        return line.split(SLIDE_TITLE[1])[0][1:]
    elif l.startswith(BULLET):
        return line[1:]
