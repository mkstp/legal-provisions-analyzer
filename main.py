# Provision Comparison Generator
# Marc St. Pierre
# 1/6/2023

import helpers
import pprint

# test globals (to be provided eventually by external input)

SOURCE_PATH = 'C:/Users/marcs/Documents/provisionsProject/Data/test.csv'
DESTINATION_PATH = 'C:/Users/marcs/Documents/provisionsProject/Data/export.csv'
SEARCH_INPUT = 'interpretation'
MATCH_THRESHOLD = 0.1


def main(csv_path, export_path, search_string, match_threshold_float, export=False, debug=True):
    search_string = helpers.cleanup(search_string)
    field_names = []
    data = helpers.collect_provisions(csv_path, search_string, match_threshold_float)
    data = helpers.sort_descending(data, -1)

    # export to csv
    if export:
        helpers.format_export(data, export_path, field_names)

    # check output
    if debug:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)


main(SOURCE_PATH, DESTINATION_PATH, SEARCH_INPUT, MATCH_THRESHOLD)

