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

EXCEL_PATH = sys.argv[1]
CLASSNAME_CACHE_PATH = sys.argv[2]
CFG_MGR_PATH = sys.argv[3]

#EXCEL_PATH = u"./excel"
#CLASSNAME_CACHE_PATH = u"./cache/classname"
#CFG_MGR_PATH = u"./cache/cplusplus_cfg_mgr"

class CTool:
    def __init__(self):
        self.mCodeData = []

    def get_code_data(self):
        return self.mCodeData

    def generate_include(self):
        code = "#pragma once" + base.change_line        
        code += "#include <cinttypes>" + base.change_line
        code += "#include <memory>" + base.change_line
        code +=  "#include <string>" +  base.change_line 
        code += base.empty_line
        code += "using namespace std;" + base.change_line        
        code += base.empty_line
        code += "namespace google" + base.change_line
        code += "{" + base.change_line
        code += base.one_tab + "namespace protobuf" + base.change_line
        code += base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + "class Message;" + base.change_line
        code += base.one_tab + "}" + base.change_line
        code += "}" + base.change_line
        code += base.empty_line

        self.mCodeData += code

    def generate_namespace_declare_start(self):
        code = "namespace config" + base.change_line
        code += "{" + base.change_line
        self.mCodeData += code

    def generate_class_declare(self, fileName):
        code = base.one_tab + "class" + base.one_space + fileName + "Cfg;" + base.change_line
        code += base.one_tab + "class" + base.one_space + fileName + ";" + base.change_line
        self.mCodeData += code

    def generate_namespace_declare_end(self):
        code = "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_error_string(self):
        code = base.empty_line 
        code += base.one_tab + "class ErrorString" + base.change_line 
        code += base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + "public:" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "ErrorString(const char* val) : content(val)" + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + base.end_scope + base.change_line 
        code += base.one_tab + base.empty_line 
        code += base.one_tab + base.one_tab + base.one_tab + "const char* Str()" + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + base.start_scope + base.change_line  
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return content;" + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + base.end_scope + base.change_line 
        code += base.empty_line 
        code += base.one_tab + base.one_tab + "private:" + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + "const char* content;" + base.change_line 
        code += base.one_tab + base.end_scope + ";" + base.change_line 
        code += base.empty_line 
        code += base.one_tab + "using ErrorStringPtr = shared_ptr<ErrorString>;" + base.change_line 
        code += base.one_tab + "#define CREATE_ERROR_STRING(text) make_shared<ErrorString>(text)" + base.change_line
        code += base.empty_line         
        self.mCodeData += code

    def generate_start_class(self):
        code = base.one_tab + "class ConfigMgr " + base.change_line
        code += base.one_tab + "{" + base.change_line
        code += base.one_tab + "public:" + base.change_line
        code += base.one_tab + base.one_tab + "~ConfigMgr();" + base.change_line
        code += base.empty_line
        code += base.one_tab + base.one_tab + "const char* GetPath();" + base.change_line
        code += base.empty_line
        code += base.one_tab + base.one_tab + "ErrorStringPtr LoadAllCfg(const char *path);" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_define_load_static(self):
        code = base.one_tab + base.one_tab + "static bool LoadExcelConfig(const char *path, google::protobuf::Message *msg);" + base.change_line
        code += base.empty_line        
        self.mCodeData += code
    
    def generate_define_reload_static(self):
        code = base.one_tab + base.one_tab + "static google::protobuf::Message* ReloadExcelConfig(const char *path,string file_name);" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_context_class(self, fileName):        
        code = base.one_tab + base.one_tab + "const " + fileName + "Cfg*  " + "Get" + fileName + "Cfg();" + base.change_line
        code += base.empty_line
        code += base.one_tab + base.one_tab + "const " + fileName + "*  " + "Get" + fileName + "ByID(uint32_t id);" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_get_by_key_name_declare(self, class_name,key_type,key_name):
        lower_key_name = key_name.lower()    
        class_name_cfg = class_name + "Cfg"        
        code = base.one_tab + base.one_tab + "const " + class_name + "* Get" + class_name + "By" + key_name + "(" + self.type_to_cplusplus_type(key_type)  + base.one_space + lower_key_name + "); " + base.change_line
        code += base.empty_line
        self.mCodeData += code         

    def generate_get_by_mix_key_names_declare(self,class_name,mixkey_types,mixkey_names):
        class_name_cfg = class_name + "Cfg"        
        code = base.one_tab + base.one_tab + "const " + class_name + "* Get" + class_name + "ByMixKey("
        i = 0
        for mix_key in mixkey_types:    
            if i == 0:        
                code += self.type_to_cplusplus_type(mixkey_types[i])  +  base.one_space + mixkey_names[i].lower()
            else:
                code += "," + self.type_to_cplusplus_type(mixkey_types[i])  +  base.one_space + mixkey_names[i].lower()
            i = i + 1
        code += "); " + base.change_line
        code += base.empty_line
        self.mCodeData += code
    
    def generate_define_start(self):
        code = base.one_tab + "private:" + base.change_line
        code += base.one_tab + base.one_tab + "const char*  path = nullptr;" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_define_class(self, fileName):
        lower_file_name = fileName.lower() 
        code = base.one_tab + base.one_tab + "" + fileName + "Cfg *" + lower_file_name + "cfg_ptr = nullptr;" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_end_class(self):
        code = base.one_tab + "};" + base.change_line
        code += base.empty_line
        code += base.one_tab + "extern shared_ptr<ConfigMgr> GConfigMgr;"
        code += base.empty_line
        self.mCodeData += code

    def generate_cpp_include(self):
        code = "#include \"configmgr.h\"" + base.change_line
        code += "#include \"google/protobuf/message.h\"" + base.change_line        
        code += "#include <fstream>" + base.change_line
        code += "#include <iostream>" + base.change_line
        code += "#include <sstream>" + base.change_line        
        self.mCodeData += code
    
    def generate_cpp_include_filename(self,fileName):
        code = "#include \"" + fileName + "\"" + base.change_line
        code += base.empty_line
        self.mCodeData += code
    
    def generate_cpp_define_var(self):        
        code = base.empty_line
        code += base.one_tab + "shared_ptr<ConfigMgr> GConfigMgr = make_shared<ConfigMgr>();" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_cpp_destruct_start(self):
        code = base.one_tab +  "ConfigMgr::~ConfigMgr()" + base.change_line
        code += base.one_tab +  "{" + base.change_line
        self.mCodeData += code

    def generate_cpp_destruct(self, fileName):
        lower_file_name = fileName.lower()
        code = base.one_tab +  base.one_tab + "if(" + lower_file_name + "cfg_ptr)" + base.change_line
        code += base.one_tab +  base.one_tab  + base.start_scope + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + "delete"+ base.one_space + lower_file_name + "cfg_ptr;" + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + lower_file_name + "cfg_ptr" + base.one_space + "=" + base.one_tab + "nullptr;" + base.change_line
        code += base.one_tab +  base.one_tab + base.end_scope + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_cpp_destruct_end(self):
        code = base.one_tab +  "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_cpp_load_template(self):
        code = base.one_tab +  "bool ConfigMgr::LoadExcelConfig(const char *path, google::protobuf::Message *msg)" + base.change_line
        code += base.one_tab +  "{" + base.change_line        
        code += base.one_tab +  base.one_tab + "ifstream ifs(path,ifstream::binary);" + base.change_line
        code += base.one_tab +  base.one_tab + "if (!ifs.is_open())" + base.change_line
        code += base.one_tab +  base.one_tab + "{" + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + "return false;" + base.change_line
        code += base.one_tab +  base.one_tab + "}" + base.change_line
        code += base.one_tab +  base.one_tab + "std::filebuf* pbuf = ifs.rdbuf();" + base.change_line 
        code += base.one_tab +  base.one_tab + "std::size_t size = pbuf->pubseekoff(0, ifs.end, ifs.in);" + base.change_line
        code += base.one_tab +  base.one_tab + "pbuf->pubseekpos(0, ifs.in);" + base.change_line
        code += base.one_tab +  base.one_tab + "char* buffer = new char[size];" + base.change_line 
        code += base.one_tab +  base.one_tab + "pbuf->sgetn(buffer, size);" + base.change_line 
        code += base.one_tab +  base.one_tab + "ifs.close();" + base.change_line
        code += base.one_tab +  base.one_tab + "bool flag = msg->ParseFromArray((const void*)buffer, size);" + base.change_line
        code += base.one_tab +  base.one_tab + "delete[] buffer;" + base.change_line
        code += base.one_tab +  base.one_tab + "return flag;" + base.change_line
        code += base.one_tab +  "}" + base.change_line
        code += base.empty_line        
        self.mCodeData += code

    def generate_cpp_load_reload_template(self):
        code = base.one_tab + "google::protobuf::Message* ConfigMgr::ReloadExcelConfig(const char *path,string file_name)" + base.change_line
        code += base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + "string prefix_path(path);" + base.change_line 
        code += base.one_tab + base.one_tab + "string path = prefix_path + \"/\" + file_name + \".pb\";" + base.change_line 
        code += base.one_tab + base.one_tab + "obj := ClassFactory::Instance()->GetClassByName(file_name)" + base.change_line
        code += base.one_tab + base.one_tab + "if (ConfigMgr::LoadExcelConfig(path.c_str(),(google::protobuf::Message*)obj))" + base.change_line
        code += base.one_tab + base.one_tab + base.start_scope + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "return (google::protobuf::Message*)obj" + base.change_line
        code += base.one_tab + base.one_tab + base.end_scope + base.change_line 
        code += base.empty_line                 
        code += base.one_tab + base.one_tab + "return nullptr;" + base.change_line 
        code += base.one_tab + base.end_scope + base.change_line
        code += base.empty_line     
        self.mCodeData += code    

    def generate_load_all_cfg_start(self):
        code = base.one_tab +  "const char* ConfigMgr::GetPath() {" + base.change_line
        code += base.one_tab +  base.one_tab + "return path;" + base.change_line
        code += base.one_tab +  "}" + base.change_line
        code += base.empty_line
        code += base.one_tab +  "ErrorStringPtr ConfigMgr::LoadAllCfg(const char *path)" + base.change_line
        code += base.one_tab +  "{" + base.change_line
        code += base.one_tab +  base.one_tab + "this->path = path;" + base.change_line
        code += base.one_tab +  base.one_tab + "string prefix_path(path);" + base.change_line
        self.mCodeData += code

    def generate_load_all_cfg(self, fileName):
        lower_file_name = fileName.lower()
        code = base.one_tab +  base.one_tab + lower_file_name + "cfg_ptr = new " + fileName + "Cfg();" + base.change_line        
        code += base.one_tab +  base.one_tab + "string " + lower_file_name + "_path = prefix_path + \"/" + fileName + ".pb\";" + base.change_line
        code += base.one_tab +  base.one_tab + "if (!ConfigMgr::LoadExcelConfig(" + lower_file_name + "_path.c_str(), " + lower_file_name + "cfg_ptr))" + base.change_line
        code += base.one_tab +  base.one_tab + "{" + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + "return CREATE_ERROR_STRING(\"load " + fileName + "  file error..\"); " + base.change_line
        code += base.one_tab +  base.one_tab + "}" + base.change_line        
        code += base.empty_line

        self.mCodeData += code

    def generate_load_all_cfg_end(self):
        code = base.one_tab + base.one_tab + "return nullptr;" + base.change_line
        code += base.one_tab +  "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_get_cfg(self, fileName): 
        lower_file_name = fileName.lower()       
        code = base.one_tab +  "const " + fileName + "Cfg* ConfigMgr::Get" + fileName + "Cfg()" + base.change_line
        code += base.one_tab +  "{" + base.change_line
        code += base.one_tab +  base.one_tab + "return " + lower_file_name + "cfg_ptr;" + base.change_line
        code += base.one_tab +  "}" + base.change_line
        code += base.empty_line

        code += base.one_tab +  "const " + fileName + "*  ConfigMgr::Get" + fileName + "ByID(uint32_t id) " + base.change_line
        code += base.one_tab +  "{" + base.change_line
        code += base.one_tab +  base.one_tab + "if (" + lower_file_name + "cfg_ptr) {" + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + "auto iter = " + lower_file_name + "cfg_ptr->datas().find(id);" + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + "if (iter != " + lower_file_name + "cfg_ptr->datas().end()) {" + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + base.one_tab + "return &(iter->second);" + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + "}" + base.change_line
        code += base.one_tab +  base.one_tab + "}" + base.change_line
        code += base.one_tab +  base.one_tab + "return nullptr;" + base.change_line
        code += base.one_tab +  "}" + base.change_line

        code += base.empty_line
        self.mCodeData += code
    
    def type_to_cplusplus_type(self,in_type):
        if in_type == "int16":
            return "int16_t"
        elif in_type == "uint16":
            return "uint16_t"
        elif in_type == "int32":
            return "int32_t"
        elif in_type ==  "uint32":
            return "uint32_t"
        elif in_type == "int64":
            return "int64_t"
        elif in_type == "uint64":
            return "uint64_t"
        else:
            return in_type 

    def generate_get_by_key_name(self, class_name,key_type,key_name):    
        lower_key_name = key_name.lower()    
        class_name_cfg = class_name + "Cfg"        
        code = base.one_tab +  "const " + class_name + "* ConfigMgr::Get" + class_name + "By" + key_name + "(" + self.type_to_cplusplus_type(key_type)  + base.one_space + lower_key_name + ")" + base.change_line                 
        code += base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + "if (" + class_name.lower() + "cfg_ptr)" + base.change_line
        code += base.one_tab + base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + "for (auto iter = " + class_name.lower() + "cfg_ptr->datas().begin(); iter != " + class_name.lower() + "cfg_ptr->datas().end(); ++iter)"  + base.change_line
        code += base.one_tab +  base.one_tab + base.one_tab + base.start_scope + base.change_line                 
        code += base.one_tab + base.one_tab + base.one_tab +  base.one_tab + "if (iter->second." + key_name.lower() + "()" + base.one_space + "==" + base.one_space + lower_key_name + ")" +base.one_space  + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab +  base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab +  base.one_tab + base.one_tab + "return &(iter->second);" + base.change_line 
        code +=  base.one_tab + base.one_tab + base.one_tab + base.one_tab +"}" + base.change_line
        code +=  base.one_tab + base.one_tab + base.one_tab   + "}" + base.change_line        
        code +=  base.one_tab + base.one_tab + "}" + base.change_line         
        code += base.one_tab + base.one_tab + "return nullptr;" + base.change_line        
        code +=  base.one_tab  + "}" + base.change_line   
        code += base.empty_line
        self.mCodeData += code

    def generate_get_by_mix_key_names(self,class_name,mixkey_types,mixkey_names):
        class_name_cfg = class_name + "Cfg"        
        code = base.one_tab  + "const " + class_name + "* ConfigMgr::Get" + class_name + "ByMixKey("
        i = 0
        for mix_key in mixkey_types:    
            if i == 0:        
                code += self.type_to_cplusplus_type(mixkey_types[i])  +  base.one_space + mixkey_names[i].lower()
            else:
                code += "," + self.type_to_cplusplus_type(mixkey_types[i])  +  base.one_space + mixkey_names[i].lower()
            i = i + 1
        code += ") " + base.change_line        
        code += base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + "if (" + class_name.lower() + "cfg_ptr)" + base.change_line
        code += base.one_tab + base.one_tab + base.start_scope + base.change_line 
        code += base.one_tab + base.one_tab + base.one_tab + "for (auto iter = " + class_name.lower() + "cfg_ptr->datas().begin(); iter != " + class_name.lower() + "cfg_ptr->datas().end(); ++iter)"  + base.change_line        
        code += base.one_tab + base.one_tab + base.one_tab +  "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "if ((iter->second." 
        i = 0
        for mix_key in mixkey_types:    
            if i == 0:        
                code += mixkey_names[i].lower() + "()" + base.one_space + "==" + base.one_space + mixkey_names[i].lower() + ")"
            else:
                code += " && " + "(iter->second." + mixkey_names[i].lower() + "()" + base.one_space + "==" + base.one_space + mixkey_names[i].lower() + ")"
            i = i + 1
        code += ")" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return &(iter->second);" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line           
        code += base.one_tab + base.one_tab + base.one_tab  + "}" + base.change_line          
        code += base.one_tab + base.one_tab + "}" + base.change_line
        code += base.one_tab + base.one_tab +  "return nullptr;" + base.change_line
        code += base.one_tab  + "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code
    
    def generate_new_obj(self,fileName):
        code = base.one_tab + "REGISTER_REFLECTOR(" + fileName + "Cfg);"  + base.change_line
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

    # configmgr.h generate
    tool = CTool()
    tool.generate_include()

    tool.generate_namespace_declare_start()
    for classname in classnames:
        tool.generate_class_declare(classname)    
    tool.generate_error_string()

    tool.generate_start_class()
    for classname in classnames:
        #id 
        tool.generate_context_class(classname)
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
                tool.generate_get_by_key_name_declare(classname,key_type,key_name)                
            elif key_str == base.MixKey:
                #minkey
                mixkey_types.append(key_type)
                mixkey_names.append(key_name)
        if len(mixkey_types) != 0 and len(mixkey_names) != 0:            
            tool.generate_get_by_mix_key_names_declare(classname,mixkey_types,mixkey_names)            

    tool.generate_define_load_static()
    #tool.generate_define_reload_static()

    tool.generate_define_start()
    for classname in classnames:
        tool.generate_define_class(classname)
    tool.generate_end_class()
    tool.generate_namespace_declare_end()

    all_path_file_name = CFG_MGR_PATH + "/" + "configmgr.h"
    with open(all_path_file_name, 'wb') as data_file:
        data_file.write(''.join(tool.get_code_data()))    
    print "configmgr.h ok"

    # configmgr.cpp generate
    cpp_tool = CTool()
    cpp_tool.generate_cpp_include()
    for _, _, files in os.walk(EXCEL_PATH):
        for filename in files:
            file_full_path = os.path.join(EXCEL_PATH, filename)
            if os.path.exists(file_full_path):
                pb_name = filename.replace(base.file_suffix_with_spot, ".pb.h")          
                cpp_tool.generate_cpp_include_filename(pb_name)

    cpp_tool.generate_namespace_declare_start()    
    cpp_tool.generate_cpp_define_var()
    cpp_tool.generate_cpp_destruct_start()
    for classname in classnames:
        cpp_tool.generate_cpp_destruct(classname)
    cpp_tool.generate_cpp_destruct_end()

    cpp_tool.generate_cpp_load_template()
    #cpp_tool.generate_cpp_load_reload_template()

    cpp_tool.generate_load_all_cfg_start()
    for classname in classnames:
        cpp_tool.generate_load_all_cfg(classname)
    cpp_tool.generate_load_all_cfg_end()

    for classname in classnames:    
        cpp_tool.generate_get_cfg(classname)   
    
    #get key minkey
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
                cpp_tool.generate_get_by_key_name(classname,key_type,key_name)
            elif key_str == base.MixKey:
                #minkey
                mixkey_types.append(key_type)
                mixkey_names.append(key_name)
        if len(mixkey_types) != 0 and len(mixkey_names) != 0:                        
            cpp_tool.generate_get_by_mix_key_names(classname,mixkey_types,mixkey_names)

    #for classname in classnames:
    #    cpp_tool.generate_new_obj(classname)

    cpp_tool.generate_namespace_declare_end() 
    
    all_path_file_name = CFG_MGR_PATH + "/" + "configmgr.cpp"
    with open(all_path_file_name, 'wb') as data_file:
        data_file.write(''.join(cpp_tool.get_code_data()))    
    print "configmgr.cpp ok"


if __name__ == '__main__':
    Start()
