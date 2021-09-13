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

    def type_to_csharp_type(self,in_type):
        if in_type == "int16":
            return "Int16"
        elif in_type == "uint16":
            return "UInt16"
        elif in_type == "int32":
            return "Int32"
        elif in_type ==  "uint32":
            return "UInt32"
        elif in_type == "int64":
            return "Int64"
        elif in_type == "uint64":
            return "UInt64"
        else:
            return in_type 

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

    def generate_get_by_key_name(self, class_name,key_type,key_name):    
        lower_key_name = key_name.lower()    
        class_name_cfg = class_name + "Cfg"        
        code = base.one_tab + base.one_tab + "public" + base.one_space + class_name + " Get" + class_name + "By" + key_name + "(" + self.type_to_csharp_type(key_type)  + base.one_space + lower_key_name + ") " + base.change_line
        code += base.one_tab + base.one_tab + "{" + base.change_line                
        code += base.one_tab + base.one_tab + base.one_tab +  "foreach (" + class_name + " val in " + class_name_cfg +".Datas.Values)" +base.empty_line
        code += base.one_tab + base.one_tab + base.one_tab +  "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab +  base.one_tab + "if (val." + key_name + base.one_space + "==" + base.one_space + lower_key_name + ")" +base.one_space  + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab +  base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab +  base.one_tab + base.one_tab + "return val;" + base.change_line 
        code +=  base.one_tab + base.one_tab + base.one_tab + base.one_tab +"}" + base.change_line
        code +=  base.one_tab + base.one_tab + base.one_tab   + "}" + base.change_line        
        code += base.one_tab + base.one_tab + base.one_tab   +  "return null;" + base.change_line        
        code +=  base.one_tab + base.one_tab  + "}" + base.change_line   
        code += base.empty_line
        self.mCodeData += code
    
    def generate_get_by_mix_key_names(self,class_name,mixkey_types,mixkey_names):
        class_name_cfg = class_name + "Cfg"        
        code = base.one_tab + base.one_tab + "public" + base.one_space + class_name + " Get" + class_name + "ByMixKey("
        i = 0
        for mix_key in mixkey_types:    
            if i == 0:        
                code += self.type_to_csharp_type(mixkey_types[i])  +  base.one_space + mixkey_names[i].lower()
            else:
                code += "," + self.type_to_csharp_type(mixkey_types[i])  +  base.one_space + mixkey_names[i].lower()
            i = i + 1
        code += ") " + base.change_line
        code += base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab +  "foreach (" + class_name + " val in " + class_name_cfg +".Datas.Values)" + base.empty_line
        code += base.one_tab + base.one_tab + base.one_tab +  "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "if ((val." 
        i = 0
        for mix_key in mixkey_types:    
            if i == 0:        
                code += mixkey_names[i] + base.one_space + "==" + base.one_space + mixkey_names[i].lower() + ")"
            else:
                code += " && " + "(val." + mixkey_names[i] + base.one_space + "==" + base.one_space + mixkey_names[i].lower() + ")"
            i = i + 1
        code += ")" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return val;" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line           
        code += base.one_tab + base.one_tab + base.one_tab  + "}" + base.change_line          
        code += base.one_tab + base.one_tab + base.one_tab + "return null;" + base.change_line
        code += base.one_tab + base.one_tab + "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

def Start():
    if os.path.exists(CFG_MGR_PATH): shutil.rmtree(CFG_MGR_PATH)    
    if not os.path.exists(CFG_MGR_PATH): os.makedirs(CFG_MGR_PATH)

    classname_content=""
    classname_file_name = CLASSNAME_CACHE_PATH + "/classname.txt"
    with open(classname_file_name, "r") as classname_file:
        classname_content = classname_file.read()
    classname_content = base.get_handle_string(classname_content)
    classnames = base.parse_classnames(classname_content)
    classnames.remove("")

    tool = CTool()
    tool.generate_include()
    tool.generate_class_start()

    tool.generate_load_all_cfg_start()
    for classname in classnames:
        tool.generate_load_all_cfg(classname)    
    tool.generate_load_all_cfg_end()

    tool.generate_load_cfg()

    #id
    for classname in classnames:
        tool.generate_get_cfg(classname)
        tool.generate_get_cfg_by_id(classname)
    #get key minkey
    classname_units = re.split(";",classname_content)
    classname_units.remove("")
    for classname_unit in classname_units:
        classname_array = re.split(":",classname_unit)
        classname = classname_array[0]
        keys=[]
        mixkey_types=[]
        mixkey_names=[]
        key_arrays = re.split("#",classname_array[1])
        for key_array in key_arrays:
            key_infos = re.split("_",key_array)
            key_str = key_infos[0]
            key_type = key_infos[1]
            key_name = key_infos[2]
            if key_name != "ID" and key_str == base.MainKey:            
                #key
                tool.generate_get_by_key_name(classname,key_type,key_name)
            elif key_str == base.MixKey:
                #minkey
                mixkey_types.append(key_type)
                mixkey_names.append(key_name)
        if len(mixkey_types) != 0 and len(mixkey_names) != 0:
            tool.generate_get_by_mix_key_names(classname,mixkey_types,mixkey_names)

    for classname in classnames:        
        tool.generate_define_class(classname)

    tool.generate_class_end()
    
    all_path_file_name = CFG_MGR_PATH + "/" + "configmgr.cs"
    with open(all_path_file_name, 'wb') as data_file:
        data_file.write(''.join(tool.get_code_data()))
    print "configmgr.cs ok"

if __name__ == '__main__':
    Start()
