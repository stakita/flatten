'''flatten.py
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


class FlattenHandlers:

    def handler_dump_sub_branch_json(branch_path, node_content, separator='.'):
        print('handler_dump_sub_branch(%s,%s)' % (branch_path, node_content))
        output_elements = {}
        output_elements[branch_path] = json.dumps(node_content)
        return output_elements


    def handler_dump_sub_branch(branch_path, node_content, separator='.'):
        print('handler_dump_sub_branch(%s,%s)' % (branch_path, node_content))
        output_elements = {}
        output_elements[branch_path] = node_content
        return output_elements


    def handler_transform_forgery_tests(branch_path, node_content, separator='.'):
        output_elements = {}

        # XXX assert node_content is list
        summary_label = branch_path + '[]'
        output_elements[summary_label] = len(node_content)

        for element in node_content:
            transformed_node_name = '%s.%s' % (element['ForgeryType'], element['ForgerySubtype'])
            transformed_node_name = transformed_node_name.replace(' ', '_')
            transformed_node_name = branch_path + separator + transformed_node_name
            output_elements[transformed_node_name] = element['TestResult']

        return output_elements


class FlattenException(Exception):
    pass

class Flatten:

    def __init__(self, flags_fields_dict=dict(), node_handlers=dict(), logging=False, expand_flagset=True):
        self.flags_fields_dict = flags_fields_dict
        self.node_handlers = node_handlers
        self.expand_flagset = expand_flagset
        self.logging = logging
        self.log_buffer = ''
        self._log() # clear the log


    def _log(self, message=None):
        if message is None: # clear the log
            self.log_buffer = ''
        elif self.logging:
            self.log_buffer += '%s\n' % message


    def _log_print(self):
        print(self.log_buffer)


    def flatten_json(self, nested_json):
        # Flatten json object with nested keys into a single level.
        # Args:
        #     nested_json: A nested json object.
        # Returns:
        #     The flattened json object if successful, None otherwise.
        self._log() # clear the log
        out = {}
        separator = '.'
        self._log('flatten_json: [separator:"%s"] - start ' % separator)

        def flatten(node, name='', separator='_'):
            self._log('flatten_json.flatten: node:%s, name:%s' % (node, name))

            if name in self.node_handlers:
                self._log('handler node')
                handler = self.node_handlers[name]
                output_elements = handler(name, node, separator=separator)
                out.update(output_elements)
            else:
                if type(node) is dict:
                    # handle recursive dictionary elements
                    self._log('recurse dict node')
                    for element in node:
                        flatten(node[element], name + separator + element,  separator=separator)
                elif type(node) is list:
                    if name in self.flags_fields_dict:
                        self._log('process list as flags field node')
                        # handle lists as flag sets
                        # check if the element is in the flags set
                        for element in node:
                            if element not in self.flags_fields_dict[name]:
                                raise FlattenException('Error in field "%s": value "%s" not in flags specification' % (name, element))
                            if not self.expand_flagset:
                                # minimal flags output here
                                out[name + '[]_%s' % element] = True

                        if self.expand_flagset:
                            # expanded flags output here
                            # iterate through the flags set and generate appropriate flag results
                            for flag in self.flags_fields_dict[name]:
                                if flag in node:
                                    out[name + '[]_%s' % flag] = True
                                else:
                                    out[name + '[]_%s' % flag] = False
                    else:
                        self._log('process list as normal node')
                        # handle lists as normal recursive element
                        # here we add an element to indicate length to make zero lenghth lists visible
                        out[name + '[]'] = len(node)
                        i = 0
                        for element in node:
                            flatten(element, name + '[%d]' % i, separator=separator)
                            i += 1
                else:
                    self._log('process primitive type node')
                    # handle node with other normal types
                    out[name] = node

        flatten(nested_json, separator=separator)
        return out



if __name__ == '__main__':
    import json
    import pprint
    import test
    j = json.loads(test.s)
    # s = '[1,2,3,{"cat": "spot", "dog":"fifi"}]'
    # s = '{"[0]":1, "[1]":2, "[2]": 3, "[3]": {"cat": "spot", "dog":"fifi"}, "[]":4 }'
    # j = json.loads(s)
    flattener = Flatten(preserve_fields, flags_lists, logging=False, expand_flagset=True)
    f = flattener.flatten_json(j)
    # pprint.pprint(f)
    print(json.dumps(j, sort_keys=True, indent=4, separators=(',', ': ')))
    print(json.dumps(f, sort_keys=True, indent=4, separators=(',', ': ')))
    # flattener._log_print()

