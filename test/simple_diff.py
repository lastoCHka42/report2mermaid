#!/usr/bin/python3

from difflib import unified_diff

import subprocess
import pytest


cmd = [
    'python3', 'main.py',
    '--input-file', 'test/input_file.txt',
    '--output-file', 'result_file.txt',
]

def test_simple_diff():
    subprocess.run(cmd)

    with open('result_file.txt', 'r') as fh:
        actual_result_lines = fh.readlines()
    with open('test/expected_result.txt', 'r') as fh:
        expectes_result_lines = fh.readlines()

    subprocess.run(['rm', 'result_file.txt'])

    diff = list(unified_diff(actual_result_lines, expectes_result_lines))
    assert diff == [], "Unexpected file contents:\n" + "".join(diff)
