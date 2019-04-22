import os
import re
import shutil

import sql_utils

def compile(path):
    files = os.listdir(path)
    for fi in files:
        fi_d = os.path.join(path, fi)            
        if os.path.isdir(fi_d):
            compile(fi_d)              
        else:
            if fi_d.split(".")[-1] in ["c", "h"]:
                try:
                    asm = Assembler(fi_d)
                    asm.compile()
                except:
                    print("Fail compile file %s" % (fi_d))  

class Assembler(object):
    arch = [
    "x86_64",
    "arm64"
    ]
    pat_code = {
        "x86_64": "([^\\n]*?# -- Begin function[\\s\\S]*?# -- End function)",
        "arm64" : "([^\\n]*?// -- Begin function[\\s\\S]*?// -- End function)"
    }
    pat_name = {
        "x86_64": "# -- Begin function ([^\\n]*)",
        "arm64": "// -- Begin function ([^\\n]*)"
    }

    def __init__(self, path):
        self._db = sql_utils.SQL.instance()
        self._path = path
        self._work_dir = "tmp"
        self._cache = dict()
        self._fun = list()
        for arch_name in self.arch:
            self._cache[arch_name] = dict()
    
    def check_file(self):
        '''
        1. Check input file exist
        2. Clean workspace.
        '''
        if self._path.split(".")[-1] != "c":
            print("Error: file %s is not c source code." % (self._path))
            return False
        if not os.path.exists(self._path):
            print("Error: file %s is not exist." % (self._path))
            return False
        if os.path.exists(self._work_dir):
            shutil.rmtree(self._work_dir)
        os.makedirs(self._work_dir)
        return True
    
    def compile(self):
        if not self.check_file():
            return
        for arch_i in self.arch:
            output = os.path.join(self._work_dir, arch_i)
            os.system("clang %s -S --target=%s -o %s" % (
                self._path, arch_i, output))
        
            asm_file = open(output).read()
            self.get_inner_code(arch_i, asm_file)
        for name in self._fun:
            if name not in self._cache["x86_64"] or\
                name not in self._cache["arm64"]:
                continue
            self._db.insert_origin(
                name,
                self._cache["x86_64"][name],
                self._cache["arm64"][name])
                
    def get_inner_code(self, arch_i, asm_file):
        codes = re.findall(self.pat_code[arch_i], asm_file)
        for code in codes:
            name = re.findall(self.pat_name[arch_i], code)
            if len(name) == 1:
                name = name[0]
                self._cache[arch_i][name] = code
                self._fun.append(name)
                print("Found func %s." % (name))

    def __repr__(self):
        return str(self.arch)

if __name__ == "__main__":
    asm = Assembler()
