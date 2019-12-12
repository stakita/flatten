import json
import pprint
import test

from scripts.flatten import flatten



if __name__ == '__main__':

    # infile_path = 'test_data/data.json'
    infile_path = 'test_data/CHL_RUN.json'

    with open(infile_path) as f:
        s = f.read()
    j = json.loads(s)
    # s = '[1,2,3,{"cat": "spot", "dog":"fifi"}]'
    # s = '{"[0]":1, "[1]":2, "[2]": 3, "[3]": {"cat": "spot", "dog":"fifi"}, "[]":4 }'
    # j = json.loads(s)


    flags_nodes = {
        '.DocumentStatusReport2.ProcessingResultRemarks': [0, 20, 40, 60, 80, 100, 120, 130, 140, 150, 160, 180, 200, 220, 260, 280, 300, 320, 340, 360, 380],
        '.PageAsSeparateDocumentProcessingReports[0].DocumentStatusReport2.ProcessingResultRemarks': [0, 20, 40, 60, 80, 100, 120, 130, 140, 150, 160, 180, 200, 220, 260, 280, 300, 320, 340, 360, 380],
        '.PageAsSeparateDocumentProcessingReports[1].DocumentStatusReport2.ProcessingResultRemarks': [0, 20, 40, 60, 80, 100, 120, 130, 140, 150, 160, 180, 200, 220, 260, 280, 300, 320, 340, 360, 380],
    }

    def handler_transform_forgery_tests(branch_path, node_content, separator='.'):
        output_elements = {}

        for element in node_content:
            transformed_node_name = '%s.%s' % (element['ForgeryType'], element['ForgerySubtype'])
            transformed_node_name = transformed_node_name.replace(' ', '_')
            transformed_node_name = branch_path + separator + transformed_node_name
            output_elements[transformed_node_name] = element['TestResult']

        return output_elements


    node_handlers = {
        '.ProcessingResult.ForgeryTests' : flatten.FlattenHandlers.handler_transform_forgery_tests,
        '.PageAsSeparateDocumentProcessingReports[0].ProcessingResult.ForgeryTests':  flatten.FlattenHandlers.handler_transform_forgery_tests,
        '.PageAsSeparateDocumentProcessingReports[1].ProcessingResult.ForgeryTests':  flatten.FlattenHandlers.handler_transform_forgery_tests,
    }

    flattener = flatten.Flatten(flags_nodes, node_handlers=node_handlers, logging=False, expand_flagset=True)
    f = flattener.flatten_json(j)

    print(json.dumps(j, sort_keys=True, indent=4, separators=(',', ': ')))
    print(json.dumps(f, sort_keys=True, indent=4, separators=(',', ': ')))
    # flattener._log_print()
