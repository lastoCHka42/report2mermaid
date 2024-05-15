# fill the dict with {index: indents_count} for indents show the level in graph
from main import debug_mode

def generate_index_to_level_dict(source):
    result = dict()
    for i in range(len(source)):
        if not len(source[i].strip()):
            continue
        indents = len(source[i]) - len(source[i].lstrip())
        result.update({i: indents})
    return(result)


def find_parent(index, indents, INDEX_TO_LEVEL):
    index_to_level_items = INDEX_TO_LEVEL.items()
    b = list(filter(lambda x: x[0] < index and x[1] == indents - 2,
                    index_to_level_items))
    if len(b) == 1:
        return(b[0])
    if len(b) > 1:
        return(sorted(list(b), key=lambda x: x[1])[-1])


def debug(line):
    if not debug_mode:
        pass
    else:
        print(line)
