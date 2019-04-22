import re
import sql_utils

STACK_OFFSET = "OFST"
LABEL = "LBL"
USED_LABEL = "ULBL"
NUMBER = "NUM"

def process():
    sql = sql_utils.SQL.instance()
    num = sql.get_source_num()

    offset = 0
    while offset < num:
        print("PreProcess has done %s / %s." % (offset, num))
        source_code = sql.fetch_origin(100, offset)
        offset += 100
        for sample in source_code:
            x86code = X86Code(sample[2])
            x86code.process()
            armcode = ArmCode(sample[3])
            armcode.process()
            sql.insert_train(sample[1],
                            x86code.to_str(),
                            armcode.to_str())
    return

def cut_line(codeObj):
    codeObj._code = codeObj._code.split("\n")
    codeObj._code = [line.strip() for line in codeObj._code]
    return

def remove_notes_x86(codeObj):
    newCode = list()
    for line in codeObj._code:
        newLine = line.split("#")[0].strip()
        if len(newLine) > 0:
            newCode.append(newLine)
    codeObj._code = newCode
    return

def remove_notes_arm(codeObj):
    newCode = list()
    for line in codeObj._code:
        newLine = line.split("//")[0].strip()
        if len(newLine) > 0:
            newCode.append(newLine)
    codeObj._code = newCode
    return

def remove_sys_code(codeObj):
    newCode = list()
    for line in codeObj._code:
        if line.strip()[0] != ".":
            newCode.append(line)
    codeObj._code = newCode
    return

def norm_stack_param_x86(codeObj):
    newCode = list()
    for line in codeObj._code:
        newLine = re.sub("$[-]*[0x]*[\\da-fA-F]+", STACK_OFFSET, line)
        newCode.append(newLine)
    codeObj._code = newCode
    return

def norm_stack_param_arm(codeObj):
    newCode = list()
    for line in codeObj._code:
        newLine = re.sub("#[-]*[0x]*[\\da-fA-F]+", STACK_OFFSET, line)
        newCode.append(newLine)
    codeObj._code = newCode
    return

def norm_save_labels(codeObj):
    newCode = list()
    for line in codeObj._code:
        if line[-1] == ":":
            newCode.append(LABEL)
            codeObj._labels.add(line[:-1])
        else:
            newCode.append(line)
    codeObj._code = newCode
    return

def remove_used_labels(codeObj):
    newCode = list()
    for line in codeObj._code:
        chunks = line.split()
        newChunks = list()
        for chunk in chunks:
            if chunk not in codeObj._labels:
                newChunks.append(chunk)
            else:
                newChunks.append(USED_LABEL)
        newLine = " ".join(newChunks)
        newCode.append(newLine)
    codeObj._code = newCode
    return

def norm_numbers(codeObj):
    newCode = list()
    for line in codeObj._code:
        newLine = re.sub("-?(((0x)[\\da-fA-F]+)|(\\d+))", NUMBER, line)
        newCode.append(newLine)
    codeObj._code = newCode
    return

def merge_chunks(codeObj):
    newCode = list()
    for line in codeObj._code:
        newLine = "_".join(line.split())
        newCode.append(newLine)
    codeObj._code = newCode
    return

class X86Code(object):
    def __init__(self, code):
        self._code = code
        self._labels = set()
        self._methods = [
            cut_line,
            remove_notes_x86,
            norm_save_labels,
            remove_used_labels,
            remove_sys_code,
            norm_stack_param_x86,
            norm_numbers,
            merge_chunks
        ]
    
    def process(self):
        for method in self._methods:
            method(self)

    def to_str(self):
        return "\n".join(self._code)

class ArmCode(object):
    def __init__(self, code):
        self._code = code
        self._labels = set()
        self._methods = [
            cut_line,
            remove_notes_arm,
            norm_save_labels,
            remove_used_labels,
            remove_sys_code,
            norm_stack_param_arm,
            norm_numbers,
            merge_chunks
        ]
    
    def process(self):
        for method in self._methods:
            method(self)

    def to_str(self):
        return "\n".join(self._code)