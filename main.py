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
    agreements = helpers.collect_agreements(source_path)
    field_names = agreements[0] + ['Search Terms'] + ['Search Score']
    data = agreements[1]
    provisions = [row[7] for row in data]
    cluster_map = sorted(helpers.cluster_provisions(provisions))

    print("Compiling search results...")
    export = helpers.format_export(field_names, data, cluster_map)

    for row in export:
        search_score = helpers.check_similar(search_string, row['Search Terms'])
        row['Search Score'] = search_score

    export = sorted(export, key=lambda item: item['Search Score'], reverse=True)

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

