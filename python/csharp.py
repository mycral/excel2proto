#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import sys
import xlrd
import string
import base
import shutil 
import re

CLASSNAME_CACHE_PATH = sys.argv[1]
CFG_MGR_PATH = sys.argv[2]

#CLASSNAME_CACHE_PATH = u"./cache/classname"
#CFG_MGR_PATH = u"./cache/csharp_cfg_mgr"

class CTool:
    def __init__(self):
        self.mCodeData = []

    def get_code_data(self):
        return self.mCodeData

    def generate_include(self):
        code = "using System;" + base.change_line
        code += "using Google.Protobuf;" + base.change_line
        code += "using Config;" + base.change_line
        code += "using System.IO;" + base.change_line        
        code += base.empty_line
        self.mCodeData += code

    def generate_class_start(self):
        code = "namespace Config {" + base.change_line
        code += base.one_tab + "public class ErrorString" + base.change_line
        code += base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + "public ErrorString(string val)" + base.change_line
        code += base.one_tab + base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + "str = " + "val;" + base.change_line
        code += base.one_tab + base.one_tab + base.end_scope + base.change_line 
        code += base.one_tab + base.one_tab + "public string Str()" + base.change_line 
        code += base.one_tab + base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + "return str;" + base.change_line 
        code += base.one_tab + base.one_tab + base.end_scope
        code += base.empty_line 
        code += base.one_tab + base.one_tab + "private string str;" + base.change_line 
        code += base.one_tab + base.end_scope + base.change_line 
        code += base.empty_line 

        code += base.one_tab + "public class ConfigMgr" + base.change_line
        code += base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + "public static ConfigMgr Instance = new ConfigMgr();" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_class_end(self):
        code =  base.one_tab + "}" + base.change_line
        code += "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_load_all_cfg_start(self):
        code = base.one_tab + base.one_tab + "public ErrorString LoadAllCfg(string prefix_path)" + base.change_line
        code += base.one_tab + base.one_tab + "{" + base.change_line
        self.mCodeData += code

    def generate_load_all_cfg(self, fileName):
        lower_file_name = fileName.lower()
        code = base.one_tab + base.one_tab + base.one_tab + "string " + lower_file_name + "_path = prefix_path + " + "\"/" + fileName + ".pb\";" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + fileName + "Cfg = (" + fileName + "Cfg)load_cfg<" + fileName + "Cfg>(" + lower_file_name + "_path);" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "if (" + fileName + "Cfg == null)" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return new ErrorString(\"Load " + fileName + " File Error...\");" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line        
        code += base.empty_line
        self.mCodeData += code

    def generate_load_all_cfg_end(self):
        code = base.one_tab + base.one_tab + base.one_tab + "return null;" + base.change_line
        code += base.one_tab + base.one_tab + "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_load_cfg(self):
        code = base.one_tab + base.one_tab + "private IMessage load_cfg<T>(string path) where T : IMessage<T> ,new()" + base.change_line
        code += base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "FileStream file_stream = null;" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "try" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "file_stream = File.Open(path, FileMode.Open);" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "catch(SystemException)" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "{" + base.change_line        
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "System.Console.Write(\"[ConfigMgr] Path = {0} Open File Error\",path);" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return null;" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line
        code += base.empty_line
        code += base.one_tab + base.one_tab + base.one_tab + "if (file_stream != null)" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "BinaryReader reader = new BinaryReader(file_stream);" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "if(reader != null)" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + base.one_tab + "byte[] datas = reader.ReadBytes((int)file_stream.Length);" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + base.one_tab + "MessageParser<T> parser = new MessageParser<T>(() => new T());" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return parser.ParseFrom(datas);" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line
        code += base.empty_line
        code += base.one_tab + base.one_tab + base.one_tab + "return null;" + base.change_line
        code += base.one_tab + base.one_tab + "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_define_class(self, fileName):
        code = base.one_tab + base.one_tab + "private " + fileName + "Cfg " + fileName + "Cfg = null;" + base.change_line        
        code += base.empty_line
        self.mCodeData += code

    def generate_get_cfg(self, fileName):        
        code = base.one_tab + base.one_tab + "public " + fileName + "Cfg  Get" + fileName + "Cfg()" + base.change_line
        code += base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "return " + fileName + "Cfg;" + base.change_line
        code += base.one_tab + base.one_tab + "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_get_cfg_by_id(self, fileName):        
        code = base.one_tab + base.one_tab + "public " + fileName + "  Get" + fileName + "ByID(UInt32 id)" + base.change_line
        code += base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "if (" + fileName + "Cfg.Datas.ContainsKey(id))" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return " + fileName + "Cfg.Datas[id];" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line
        code += base.empty_line
        code += base.one_tab + base.one_tab + base.one_tab + "return null;" + base.change_line
        code += base.one_tab + base.one_tab + "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code            

def Start():
    if os.path.exists(CFG_MGR_PATH): shutil.rmtree(CFG_MGR_PATH)    
    if not os.path.exists(CFG_MGR_PATH): os.makedirs(CFG_MGR_PATH)

    classname_file_name = CLASSNAME_CACHE_PATH + "/classname.txt"
    with open(classname_file_name, "r") as classname_file:
        classname_content = classname_file.read()
        classnames = re.split(base.one_space,classname_content)

    classnames.remove("")

    tool = CTool()
    tool.generate_include()
    tool.generate_class_start()

    tool.generate_load_all_cfg_start()
    for classname in classnames:
        tool.generate_load_all_cfg(classname)    
    tool.generate_load_all_cfg_end()

    tool.generate_load_cfg()
    for classname in classnames:
        tool.generate_get_cfg(classname)
        tool.generate_get_cfg_by_id(classname)
    

    for classname in classnames:        
        tool.generate_define_class(classname)

    tool.generate_class_end()
    
    all_path_file_name = CFG_MGR_PATH + "/" + "configmgr.cs"
    with open(all_path_file_name, 'wb') as data_file:
        data_file.write(''.join(tool.get_code_data()))
    print "configmgr.cs ok"

if __name__ == '__main__':
    Start()
