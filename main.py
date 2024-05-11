#!/usr/bin/python3
import argparse

from helpers.helpers import *
from helpers.node import Node


parser = argparse.ArgumentParser(description=
                                'Convert DataFusion Explain Analyze \
                                to Mermaid')
parser.add_argument('-f', '--input-file',
                    default='input_file.txt',
                    help='path to file with Explain Analyze data')
parser.add_argument('-o', '--output-file',
                    default='result.txt',
                    help='path to output file')
parser.add_argument('-d', '--debug',
                    action='store_true',
                    help='print log to stdout')
args = parser.parse_args()

debug_mode = args.debug


if __name__ == "__main__":


    nodes = dict()
    with open(args.input_file, 'r') as f:
        source = f.readlines()

    INDEX_TO_LEVEL = generate_index_to_level_dict(source)

    for i in range(len(INDEX_TO_LEVEL)):
        name, content_raw = source[i].strip().split(':', 1)
        content = (i, INDEX_TO_LEVEL[i])
        node = Node(i, name, content_raw)
        nodes.update({i: node})
        if i == 0:
            continue
        a = find_parent(*content, INDEX_TO_LEVEL)
        node.add_parent(nodes[a[0]])

    RESULT = ["graph BT\n"]
    for i, node in nodes.items():
        RESULT.append(node.mermaid_repr())
        debug(node.pprint())

    with open(args.output_file, 'w') as f:
        f.write('\n'.join(RESULT))

    print(f'Result saved to {args.output_file}')
