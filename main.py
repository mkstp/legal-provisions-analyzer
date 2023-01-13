# Provision Comparison Generator
# Marc St. Pierre
# 1/6/2023

import helpers
import pprint
import csv

# test globals (to be provided eventually by external input)

DATA_FOLDER = 'C:/Users/marcs/Documents/provisionsProject/Data/agreements/'
DESTINATION_PATH = 'C:/Users/marcs/Documents/provisionsProject/Data/export.csv'
SEARCH_INPUT = 'ratification'


def main(source_path, export_path, search_string, export_flag=False, debug_flag=True):
    search_string = helpers.cleanup(search_string)
    print("Collecting agreements...")
    agreements = helpers.collect_agreements(source_path)
    field_names = agreements[0]
    data = agreements[1]
    provisions = [row[7] for row in data]
    cluster_map = sorted(helpers.cluster_provisions(provisions))

    print("Compiling search results...")
    export = helpers.format_export(field_names, data, cluster_map)
    export = helpers.search_filter(export, search_string)
    for row in export:
        del row['Search Terms']
        del row['Search Score']

    # export to csv
    if export_flag:
        with open(export_path, 'w', newline='') as file:
            csvwriter = csv.DictWriter(file, fieldnames=field_names)
            csvwriter.writeheader()
            csvwriter.writerows(export)
        print(f"Exported to csv here:\n    {export_path}")

    # check output
    if debug_flag:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(export)


main(DATA_FOLDER, DESTINATION_PATH, SEARCH_INPUT, True, False)

