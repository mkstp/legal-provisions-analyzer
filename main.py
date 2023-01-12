# Provision Comparison Generator
# Marc St. Pierre
# 1/6/2023

import helpers
import pprint

# test globals (to be provided eventually by external input)

DATA_FOLDER = 'C:/Users/marcs/Documents/provisionsProject/Data/agreements/'
DESTINATION_PATH = 'C:/Users/marcs/Documents/provisionsProject/Data/export.csv'
SEARCH_INPUT = 'interpretation'


def main(source_path, export_path, search_string, export_flag=False, debug_flag=True):
    search_string = helpers.cleanup(search_string)
    data = helpers.collect_agreements(source_path)
    provisions = [provision[7] for provision in data]
    cluster_map = sorted(helpers.cluster_provisions(provisions))
    export = helpers.format_export(data, cluster_map)

    # export to csv
    if export_flag:
        helpers.export_csv(export[0], export_path, export[1])

    # check output
    if debug_flag:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(cluster_map)


main(DATA_FOLDER, DESTINATION_PATH, SEARCH_INPUT)

