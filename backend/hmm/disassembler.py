import json
import argparse
import pefile
import subprocess
from capstone import *

def run_command(cmd):
    proc = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.read().decode('utf-8'), proc.stderr.read().decode('utf-8')

class Disassembler():

    def __init__(self, file):
        self.file = file
        self.arch = self.get_arch()
        self.configure_environment()


    def get_arch(self):
        out, err = run_command("file "+self.file)
        out = out.split(":")[1]
        if "x86-64" in out:
            return CS_MODE_64
        else:
            return CS_MODE_32


    def find_section(self):
        for section in self.pe.sections:
            if section.contains_rva(self.base_of_code):
                return section
        return None


    def configure_environment(self):

        self.cs = Cs(CS_ARCH_X86, self.arch)
        self.pe = pefile.PE(self.file)

        self.original_entry_point = self.pe.NT_HEADERS.OPTIONAL_HEADER.AddressOfEntryPoint
        self.base_of_code = self.pe.OPTIONAL_HEADER.BaseOfCode
        self.code_section = self.find_section()

        if self.code_section is None:
            raise Exception('unable to find .text section')

        self.code_size = self.code_section.Misc_VirtualSize
        self.raw_code = self.code_section.get_data(self.base_of_code, self.code_size)


    def disassemble(self):
        return self.cs.disasm(self.raw_code, self.base_of_code)


    def disassemble_to_file(self, out_file):
        dis = self.disassemble()
        out_json = {}
        out_json["v"] = []

        for i in dis:
            out_json["v"].append(i.insn_name())

        with open(out_file, 'w') as f:
            f.write(json.dumps(out_json))
