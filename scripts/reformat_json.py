#!/usr/bin/env python3
'''reformat_json.py

Usage:
  reformat_json.py [--indent=INDENT] <INPUT_JSON> [<OUTPUT_JSON>]

Options:
  -i, --indent=INDENT    Indentation spaces (default:4)
'''

import sys
import json


try:
    from docopt import docopt
except ImportError as e:
    dependencies = ['docopt']
    sys.stderr.write('Error: %s\nTry:\n    pip install --user %s\n' % (e, ' '.join(dependencies)))
    sys.exit(1)


def main(args):
    input_filename = args['<INPUT_JSON>']
    output_filename = args['<OUTPUT_JSON>']
    indent = args['--indent']

    input_content = open(input_filename).read()
    input_json = json.loads(input_content)

    reformat_json_string = json.dumps(input_json, sort_keys=False, indent=4, separators=(',', ': '))

    if output_filename is not None:
        open(output_filename, 'w+').write(reformat_json_string)
    else:
        sys.stdout.write(reformat_json_string)

    return 0


def main_shim():
    arguments = docopt(__doc__)
    sys.exit(main(arguments))


if __name__ == '__main__':
    main_shim()