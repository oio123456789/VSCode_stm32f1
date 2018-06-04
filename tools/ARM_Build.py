

import subprocess
import os
import sys
import json


class ArmBuild:

    defs = []
    mcu = []
    includes = []
    sources = []
    user_sources = []
    diver_sources = []
    libarm = []

    x_option = ""
    option = []
    link_option = []

    compiler = ""
    objcopy = ""

    out_path = ""
    out_name = ""

    startup_file = ""
    ld_script_file = ""

    def __init__(self):

        self.x_option = "assembler-with-cpp"

    def run(self, commond):
        subprocess.run(commond, shell=True)

    def get_command(self, source_file, is_asm_file=False):

        str = self.compiler

        if is_asm_file == True:
            str += " -x " + self.x_option  # " -x assembler-with-cpp"

        for item in self.mcu:
            str += " -" + item
        for item in self.defs:
            str += " -D" + item
        for item in self.includes:
            str += " -I" + item
        for item in self.option:
            str += " -" + item

        name = os.path.split(os.path.splitext(source_file)[0])[1]
        name = os.path.join(self.out_path, name)

        str += " -c " + source_file
        str += " -MF" + "\"" + name + ".d" + "\""
        str += " -MT" + "\"" + name + ".d" + "\""
        if is_asm_file != True:
            str += " -Wa,-a,-ad,-alms=" + name + ".lst"
        str += " -o " + name+".o"
        return str

    def out_path_clear(self):
        if(os.path.exists(self.out_path) == False):
            os.makedirs(self.out_path)
            return
        for (root, dirs, files) in os.walk(self.out_path):
            for filename in files:
                # print(os.path.join(root, filename))
                os.remove(os.path.join(root, filename))

    def compiler_files(self, files, is_asm_file=False):
        for file in files:
            command = self.get_command(file, is_asm_file)
            self.run(command)

    def compiler_sources_files(self, sources):
        for file in sources:
            command = self.get_command(file)
            self.run(command)

    def compiler_user_sources_files(self):
        self.compiler_sources_files(self.user_sources)

    def compiler_diver_sources_files(self):
        self.compiler_sources_files(self.diver_sources)

    def compiler_startup_file(self):
        command = self.get_command(self.startup_file, True)
        self.run(command)

    def compiler_to_elf_file(self):
        files_o = []
        for (root, dirs, files) in os.walk(self.out_path):
            for filename in files:
                ext = os.path.splitext(filename)
                if ext[1] == ".o":
                    files_o.append(os.path.join(root, filename))

        command = self.compiler

        for file in files_o:
            command += " " + file

        # command += " -mcpu=cortex-m3 -mthumb"
        for item in self.mcu:
            command += " -" + item

        for item in self.link_option:
            command += " -" + item
        # link option
        # command += " -specs=nano.specs"
        # command += " -specs=nosys.specs"
        # command += " -u _printf_float"
        # command += " -u _scanf_float"

        for item in self.libarm:
            command += " " + item

        command += " -T" + "\"" + self.ld_script_file + "\""
        command += " -lc -lm -lnosys"
        command += " -Wl,-Map="
        command += "\"" + (os.path.join(self.out_path,
                                        self.out_name)) + ".map" + "\""
        command += ",--cref -Wl,--gc-sections"
        command += " -o " + "\"" + \
            (os.path.join(self.out_path, self.out_name)) + ".elf" + "\""
        # print(command)
        self.run(command)

    def compiler_elf_file(self):
        file = os.path.join(self.out_path, self.out_name)
        command = self.objcopy
        command += " -O ihex"
        command += " " + file + ".elf"
        command += " " + file + ".hex"
        # print(command)
        self.run(command)
        command = self.objcopy
        command += " -O binary -S"
        command += " " + file + ".elf"
        command += " " + file + ".bin"
        self.run(command)

    def load_file(self, text_body=''):
        load_dict = json.loads(text_body)
        if(load_dict == None):
            return
        configurations = load_dict['configurations'][0]

        path = configurations["path"][0]
        option = configurations["option"]
        link_option = configurations["link_option"]

        include = configurations["includePath"]
        # sources = configurations["sources"]
        defines = configurations["defines"]
        mcu = configurations["mcu"]

        user = configurations["sources"][0]["user"]
        driver = configurations["sources"][0]["driver"]
        libarm = configurations["sources"][0]["libarm"]

        self.startup_file = configurations["sources"][0]["startup_file"]
        self.ld_script_file = configurations["sources"][0]["ld_script_file"]

        self.compiler = path["compiler"]
        self.objcopy = path["objcopy"]
        self.out_path = path["out_path"]
        self.out_name = path["out_name"]

        for item in option:
            if(len(item) > 0):
                self.option.append(item)
        for item in link_option:
            if(len(item) > 0):
                self.link_option.append(item)
        for item in defines:
            if(len(item) > 0):
                self.defs.append(item)
        for item in mcu:
            if(len(item) > 0):
                self.mcu.append(item)
        for item in include:
            if(len(item) > 0):
                self.includes.append(item)
        for item in user:
            if(len(item) > 0):
                self.user_sources.append(item)
        for item in driver:
            if(len(item) > 0):
                self.diver_sources.append(item)
        for item in libarm:
            if(len(item) > 0):
                self.libarm.append(item)


# -----------------------------------------------------------------------


def run(json_path="", option="all"):
    # ---------------------------------------------------------------------------------------
    arm = ArmBuild()
    cur_path = os.path.abspath(os.path.curdir)
    # ---------------------------------------------------------------------------------------
    # file_path = ".vscode/c_cpp_properties.json"
    file_path = json_path
    with open(file_path, 'r') as file:
        text_body = file.read()

    text_body = text_body.replace("${workspaceFolder}", cur_path)
    text_body = text_body.replace("${workspaceRoot}", cur_path)

    text_body = text_body.replace("\\\\", "\\")
    text_body = text_body.replace("\\", "/")

    arm.load_file(text_body)

    if(option != "user"):
        print("clear out path")
        arm.out_path_clear()
        print("compiler diver sources file")
        arm.compiler_diver_sources_files()
        print("compiler startup file")
        arm.compiler_startup_file()

    print("compiler user sources file")
    arm.compiler_user_sources_files()

    print("compiler to elf file")
    arm.compiler_to_elf_file()
    print("generate .bin .hex file")
    arm.compiler_elf_file()


if __name__ == '__main__':
    print("start build")
    #option = "all"
    json_path = ""
    if(len(sys.argv) > 2):
        json_path = sys.argv[1]
        os.chdir(sys.argv[2])
        if(len(sys.argv) > 3):
            option = sys.argv[3]
    else:
        exit()
    run(json_path, option)
    print("end build")
