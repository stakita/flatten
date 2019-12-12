'''build_csv.py
Aggregate test results into a form for hive ingestion

Usage:
  build_csv.py <input_dir> <output_csv>
  build_csv.py (-h | --help)

Options:
  -h --help     Show this screen.
'''
import sys
import pprint
import csv
import os
import json

try:
    from docopt import docopt
except ImportError as e:
    sys.stderr.write('Error: %s\nTry:\n    pip3 install --user docopt\n' % e)
    sys.exit(1)
try:
    import sh
except ImportError as e:
    sys.stderr.write('Error: %s\nTry:\n    pip3 install --user sh\n' % e)
    sys.exit(1)


def flatten_json(nested_json):
    # Flatten json object with nested keys into a single level.
    # Args:
    #     nested_json: A nested json object.
    # Returns:
    #     The flattened json object if successful, None otherwise.
    out = {}
    separator = '.'

    def flatten(x, name='', separator='_'):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + separator, separator=separator)
        elif type(x) is list:
            # i = 0
            # for a in x:
            #     flatten(a, name + str(i) + separator)
            #     i += 1
            out[name[:-1]] = '|'.join(x)
        else:
            out[name[:-1]] = x

    flatten(nested_json, separator=separator)
    return out

def main(argv):
    input_dir = argv['<input_dir>']
    output_csv = argv['<output_csv>']
    fields = set()
    fields_sorted = None

    # Process
    #     1. go through each file to determine the field superset (maintaining hierarchy)
    #     2. generate a csv with the field superset as columns

    # 1.1 get list of files
    all_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    # pprint.pprint(all_files)

    start = None
    # 1.2 open up each file and for each
    for current_file in all_files:
        # 1.2.1 decode contents as json
        with open(current_file) as rfd:
            j = json.load(rfd)
            # pprint.pprint(j)

            # 1.2.2 iterate through the structure
            flat_j = flatten_json(j)
            # pprint.pprint(flat_j)
            # 1.2.3 add to list of hierarchical fields
            fields = fields.union(set(flat_j.keys()))
            # pprint.pprint(fields)

    fields_sorted = sorted(fields)

    # Add our reference fields
    fields_sorted = ['entity_uuid'] + fields_sorted

    pprint.pprint(fields_sorted)
    print('fields:  ', len(fields_sorted))

    # 2. generate a csv with the field superset as columns
    # 2.1 open the output file with the csv dict writer
    with open(output_csv, 'w+') as wfd:
        writer = csv.DictWriter(wfd, fields_sorted)
        # 2.2 write the header row
        writer.writeheader()

        # 2.3 iterate through each of the results
        for current_file in all_files:
            with open(current_file) as rfd:
                j = json.load(rfd)

                # 2.4 flatten the dictionary
                flat_j = flatten_json(j)

                # 2.5 extract the uuid from the customerReferenceId field - reinsert as entity_uuid
                original_path = flat_j['customerReferenceId']
                entity_uuid = original_path.split('/')[-1].split('_')[1]
                flat_j['entity_uuid'] = entity_uuid

                # 2.6 submit the dictionary to the csv writer
                writer.writerow(flat_j)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    sys.exit(main(arguments))
