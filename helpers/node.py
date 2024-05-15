import json


class Node():
    def __init__(self, index, name, content, parent=None):
        self.index = index
        self.name = name
        self.content = content
        self.parent = parent
        self.childrens = list()
        self.metrics = self.content.split('metrics=')[-1].\
            lstrip('[').rstrip(']').replace(',', '\\n')

    def __repr__(self):
        return(str(self.name))

    def content_to_json(self):
        # replace non-JSON symbols to JSON symbols, wrap strings to quotes
        symbols_to_replace = {
            ', ': '", "',
            '=': '":"',
            '[': '"{"',
            ']': '"}"',
            '""': '',
            '}"}': '}}'
        }
        self.content_processor = '{"' + self.content.strip() + '}'
        for s, d in symbols_to_replace.items():
            self.content_processor = self.content_processor.replace(s, d)

        # find all the cases of `{ no colon text }` and replace parents
        # don't start from the zero index to avoid starting JSON replace
        def replace_non_dict(start=1):
            dict_start = self.content_processor.find('{', start)
            dict_end = self.content_processor.find('}', dict_start)
            colon = self.content_processor.find(':', dict_start, dict_end)
            if colon == -1:
                self.content_processor = self.content_processor[:dict_start] +\
                    '[' + \
                    self.content_processor[dict_start + 1:dict_end] + \
                    ']' + \
                    self.content_processor[dict_end + 1:]
                print(self.content_processor)
            if not dict_start == self.content_processor.rfind('{', start):
                replace_non_dict(start=dict_end)

        replace_non_dict()
        try:
            res = json.loads(self.content_processor)
        except Exception as e:
            res = f"""
            >>>>>>>>>>>>>>>>ERROR
            {self.content_processor}
            >>>>>>>>>>>>>>>>{e}
            """
        # res = self.content_processor

        print(res)

    def add_parent(self, parent):
        self.parent = parent
        parent.childrens.append(self)

    def mermaid_repr(self):
        res = f"{self.index}[<b>{self.name}</b>\n{self.metrics}]"
        if self.parent:
            res += f" --> {self.parent.index}"
        return(res)

    def childrens_repr(self):
        if not self.childrens:
            return
        return([children.index for children in self.childrens])

    def pprint(self):
        node_description = f"""
NAME: {self.name}
CONTENT: {self.content}
PARENT: {self.parent.index if self.parent else None}
CHILDRENS: {self.childrens_repr()}
------------------------------------------------\n
"""
        return(node_description)
