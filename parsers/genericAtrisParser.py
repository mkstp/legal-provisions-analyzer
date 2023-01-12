# ATRIS Parser
# Marc St. Pierre 1/9/2023

import helpers
import pprint
import string
import requests
from bs4 import BeautifulSoup

# for tlicho, tsawwassen, and anishinabek final agreements in ATRIS

URL = 'https://www.rcaanc-cirnac.gc.ca/eng/1663876084479/1663876161241'
FILENAME = 'Anishinabek.csv'
DESTINATION_PATH = 'C:/Users/marcs/Documents/provisionsProject/Data/agreements/' + FILENAME
YEAR = '2019'
ROMAN = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
ALPHA = list(string.ascii_lowercase)
IGNORE_PART = [
    'about this site',
    'table of contents',
    'anishinabek',
    'tlicho',
    'tsawwassen',
    'chapter',
    'section',
    'subsection'
]


def parse(link, export_path, export_flag=False, debug_flag=True):
    soup = BeautifulSoup((requests.get(link)).content, 'html.parser')
    log_data = False
    provision_kernel = ''  # temp variable which holds the kernel of a provision reference
    enum_type = 'nil'
    prev_enum_type = 'nil'
    int_index = 0
    alpha_index = 0
    roman_index = 0

    field_names = [
        'Agreement',  # name of the document
        'Year',  # year the document was signed
        'Part',  # for style purposes this cannot be called a 'chapter' (but it's basically a chapter)
        'Section',  # refers to any subheading under a part heading
        'Provision Reference',  # number within the written document
        'Provision Text',  # the content of the provision
        'search_part',  # a simplified combination of part and section for search purposes
        'search_text'  # a simplified version of the provision text for search purposes
    ]

    agreement = ''
    year = YEAR
    part = ''
    section = ''
    provision_reference = ''
    provision_text = ''
    data = []

    for child in soup.main.next_elements:
        append_bullet = ''

        # case for title
        if child.name == 'h1':
            agreement = child.get_text()
            continue

        # cases for headings
        if child.name == 'h2':
            part = child.get_text()
            section = ''
            continue

        if child.name in ['h3', 'h4', 'h5', 'h6']:
            section = child.get_text()
            continue

        # case for paragraphs
        if child.name == 'p' and part.lower() not in IGNORE_PART:
            prev_enum_type = 'nil'
            log_data = True
            # check if the first word in the provision is a number
            try:
                int(child.get_text()[0])

                # if so, update the provision_num
                provision_kernel = (child.get_text().split(' ', 1)[0]).strip('\n')
                provision_reference = provision_kernel

                # update provision_text with remainder of provision
                provision_text = " ".join(child.get_text().split(' ')[1:])

            # when the first word is not a number
            except ValueError:
                provision_text = child.get_text()
                provision_reference = provision_kernel

            # when the paragraph is completely empty
            except IndexError:
                continue

        # case for list bullets
        if child.name == 'li' and part.lower() not in IGNORE_PART:
            log_data = True
            provision_text = child.get_text()

            # for numbering, update what type of bullet it is
            if 'class' in child.parent.attrs:
                # for simplicity, going to treat uppercase bullets like lower case bullets
                if 'lst-upr-alph' in child.parent.attrs['class'][0]:
                    enum_type = 'lst-lwr-alph'
                else:
                    enum_type = child.parent.attrs['class'][0]

            # 12 cases for bullet enumeration
            if enum_type == 'lst-spcd' and prev_enum_type == 'nil':
                int_index = 1  # start enumerating the numbered bullets at 1
                append_bullet = f"({int_index})"

            if 'lst-lwr-alph' in enum_type and prev_enum_type == 'nil':
                alpha_index = 0
                append_bullet = f"({int_index})({ALPHA[alpha_index]})"

            if 'lst-lwr-rmn' in enum_type and prev_enum_type == 'nil':
                roman_index = 0
                append_bullet = f"({int_index})({ALPHA[alpha_index]})({ROMAN[roman_index]})"

            if enum_type == 'lst-spcd' and prev_enum_type == 'lst-spcd':
                int_index += 1
                append_bullet = f"({int_index})"

            if 'lst-lwr-alph' in enum_type and prev_enum_type == 'lst-spcd':
                alpha_index = 0
                append_bullet = f"({int_index})({ALPHA[alpha_index]})"

            if 'lst-lwr-rmn' in enum_type and prev_enum_type == 'lst-spcd':
                roman_index = 0
                append_bullet = f"({int_index})({ALPHA[alpha_index]})({ROMAN[roman_index]})"

            if enum_type == 'lst-spcd' and 'lst-lwr-alpha' in prev_enum_type:
                int_index += 1
                append_bullet = f"({int_index})"

            if 'lst-lwr-alph' in enum_type and 'lst-lwr-alph' in prev_enum_type:
                alpha_index += 1
                append_bullet = f"({int_index})({ALPHA[alpha_index]})"

            if 'lst-lwr-rmn' in enum_type and 'lst-lwr-alph' in prev_enum_type:
                roman_index = 0
                append_bullet = f"({int_index})({ALPHA[alpha_index]})({ROMAN[roman_index]})"

            if enum_type == 'lst-spcd' and 'lst-lwr-rmn' in prev_enum_type:
                int_index += 1
                append_bullet = f"({int_index})"

            if 'lst-lwr-alph' in enum_type and 'lst-lwr-rmn' in prev_enum_type:
                alpha_index += 1
                append_bullet = f"({int_index})({ALPHA[alpha_index]})"

            if 'lst-lwr-rmn' in enum_type and 'lst-lwr-rmn' in prev_enum_type:
                roman_index += 1
                append_bullet = f"({int_index})({ALPHA[alpha_index]})({ROMAN[roman_index]})"

            prev_enum_type = enum_type
            provision_reference = provision_kernel + append_bullet

        if log_data:
            search_part = helpers.cleanup(f"{part} {section}", IGNORE_PART)
            search_text = helpers.cleanup(provision_text, IGNORE_PART)
            data.append([
                agreement,
                year,
                part,
                section,
                provision_reference,
                provision_text,
                search_part,
                search_text
            ])
            log_data = False

    # export to csv
    if export_flag:
        helpers.export_csv(data, export_path, field_names)

    # check output
    if debug_flag:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)


parse(URL, DESTINATION_PATH, True, False)


