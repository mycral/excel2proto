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
#CFG_MGR_PATH = u"./cache/go_cfg_mgr"

class CTool:
    def __init__(self):
        self.mCodeData = []

    def get_code_data(self):
        return self.mCodeData

    def generate_package(self):
        code = "package config" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_import(self):
        code = "import (" + base.change_line
        code += base.one_tab + "\"fmt\"" + base.change_line
        code += base.one_tab + "\"io/ioutil\"" + base.change_line
        code += base.one_tab + "\"os\"" + base.change_line        
        code += base.one_tab + "\"reflect\"" + base.change_line 
        code += base.one_tab + "\"github.com/golang/protobuf/proto\"" + base.change_line
        code += ")" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_start_struct(self):
        code = "type ConfigMgr struct {" + base.change_line
        code += base.one_tab + "DirPath" + base.one_space + "string" + base.change_line
        self.mCodeData += code

    def generate_context_struct(self, classname):
        classname_cfg = classname + "Cfg"        
        code = base.one_tab + classname_cfg + base.one_tab + "*" + classname_cfg + base.change_line
        self.mCodeData += code

    def generate_end_struct(self):
        code = "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code    

    def generate_load_all_cfg_start(self):
        code = "func (c *ConfigMgr) LoadAllCfg(dirPath string) error {" + base.change_line
        code += base.one_tab + "c.DirPath" + base.one_space + "=" + base.one_space + "dirPath" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_load_all_cfg_context_new_obj(self, file_name):
        class_name_cfg = file_name + "Cfg"               
        code = base.one_tab + "c." + class_name_cfg + base.one_space + "=" + base.one_space +"&" + class_name_cfg + "{}" + base.change_line
        self.mCodeData += code
    
    def generate_load_all_cfg_context_map_start(self):
        code = base.empty_line
        code += base.one_tab + "cfgs := map[string]proto.Message{" + base.change_line
        self.mCodeData += code

    def generate_load_all_cfg_context_map_middle(self,file_name):
        code = base.one_tab + base.one_tab + "\"" + file_name +"\":" + base.one_space + "c." + file_name + "Cfg," + base.change_line
        self.mCodeData += code
    
    def generate_load_all_cfg_context_map_end(self):
        code = base.one_tab + base.end_scope + base.change_line
        code += base.empty_line
        self.mCodeData += code


    def generate_load_all_cfg_context_end(self):
        code =  base.one_tab + "for fileName, msg := range cfgs {" + base.change_line
        code += base.one_tab + base.one_tab + "if err := LoadConfig(dirPath,"+ base.one_space + "fileName," + base.one_space +  "msg); err != nil {" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "return err" + base.change_line
        code += base.one_tab + base.one_tab + "}" + base.change_line
        code += base.one_tab +  "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_load_all_cfg_end(self):
        code = base.one_tab + "return nil" + base.change_line
        code += "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_get_by_id(self, class_name):        
        class_name_cfg = class_name + "Cfg"        
        code = "func (c *ConfigMgr) Get" + class_name + "ByID(id uint32) *" + class_name + " {" + base.change_line
        code += base.one_tab + "if c." + class_name_cfg + ".Datas != nil {" + base.change_line
        code += base.one_tab + base.one_tab + "if info, ok := c." + class_name_cfg + ".Datas[id]; ok {" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + "return info" + base.change_line
        code += base.one_tab + base.one_tab + "}" + base.change_line
        code += base.one_tab + "}" + base.change_line
        code += base.one_tab + "return nil" + base.change_line
        code += "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_get_by_key_name(self, class_name,key_type,key_name):    
        lower_key_name = key_name.lower()    
        class_name_cfg = class_name + "Cfg"        
        code = "func (c *ConfigMgr) Get" + class_name + "By" + key_name + "(" + lower_key_name + base.one_space + key_type + ") *"    + class_name + " {" + base.change_line
        code += base.one_tab + "if c." + class_name_cfg + ".Datas != nil {" + base.change_line
        code += base.one_tab + base.one_tab + "for _, info := range c." + class_name_cfg + ".Datas {" + base.empty_line
        code += base.one_tab + base.one_tab + base.one_tab + "if info." + key_name + base.one_space + "==" + base.one_space + lower_key_name + base.one_space + "{" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return info" + base.change_line 
        code +=  base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line
        code +=  base.one_tab + base.one_tab  + "}" + base.change_line
        code += base.one_tab + "}" + base.change_line
        code += base.one_tab + "return nil" + base.change_line
        code += "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_get_by_mix_key_names(self,class_name,mixkey_types,mixkey_names):          
        class_name_cfg = class_name + "Cfg"        
        code = "func (c *ConfigMgr) Get" + class_name + "ByMixKey("
        i = 0
        for mix_key in mixkey_types:    
            if i == 0:        
                code += mixkey_names[i].lower() +  base.one_space + mixkey_types[i]
            else:
                code += "," + mixkey_names[i].lower() +  base.one_space + mixkey_types[i]
            i = i + 1
        code += ") *"    + class_name + " {" + base.change_line
        code += base.one_tab + "if c." + class_name_cfg + ".Datas != nil {" + base.change_line
        code += base.one_tab + base.one_tab + "for _, info := range c." + class_name_cfg + ".Datas {" + base.empty_line
                
        code += base.one_tab + base.one_tab + base.one_tab + "if info." 
        i = 0
        for mix_key in mixkey_types:    
            if i == 0:        
                code += mixkey_names[i] + base.one_space + "==" + base.one_space + mixkey_names[i].lower()
            else:
                code += " && " + "info." + mixkey_names[i] + base.one_space + "==" + base.one_space + mixkey_names[i].lower()
            i = i + 1
        code += " {" + base.change_line
        code += base.one_tab + base.one_tab + base.one_tab + base.one_tab + "return info" + base.change_line 
        code +=  base.one_tab + base.one_tab + base.one_tab + "}" + base.change_line
        code +=  base.one_tab + base.one_tab  + "}" + base.change_line
        code += base.one_tab + "}" + base.change_line
        code += base.one_tab + "return nil" + base.change_line
        code += "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code

    def generate_set_cfg(self,class_name):
        class_name_cfg = class_name + "Cfg"
        code = "func (c *ConfigMgr) Set" + class_name_cfg +"(cfg *" + class_name_cfg + ")" + base.one_space + base.start_scope + base.change_line
        code += base.one_tab + "c." + class_name_cfg + base.one_space + "=" + base.one_space + "cfg" + base.change_line
        code += base.end_scope + base.change_line
        code += base.empty_line 
        self.mCodeData += code
    
    def generate_load_cfg(self):
        code = "func LoadConfig(dirPath string, fileName string, message proto.Message) error {" + base.change_line
        code += base.one_tab + "PbName := dirPath + \"/\" + fileName + \".pb\"" + base.change_line
        code += base.one_tab + "file, openErr := os.Open(PbName)" + base.change_line
        code += base.one_tab + "if openErr != nil {" + base.change_line
        code += base.one_tab + base.one_tab + "return openErr" + base.change_line
        code += base.one_tab + "}" + base.change_line
        code += base.one_tab + "defer file.Close()" + base.change_line
        code += base.one_tab + "datas, readErr := ioutil.ReadAll(file)" + base.change_line
        code += base.one_tab + "if readErr != nil {" + base.change_line
        code += base.one_tab + base.one_tab + "return readErr" + base.change_line
        code += base.one_tab + "}" + base.change_line
        code += base.one_tab + "return proto.Unmarshal(datas, message)" + base.change_line
        code += "}" + base.change_line
        code += base.empty_line
        self.mCodeData += code
    
    def generate_reload_cfg(self):
        code = "func ReloadConfig(dirPath string, fileName string) (error, proto.Message) {" + base.change_line
        code += base.one_tab + "className := fileName" + base.one_space + "+" + base.one_space + "\"Cfg\"" + base.change_line
        code += base.one_tab + "obj := GStringToStructMgr.GetStructObj(className)" + base.change_line
        code += base.one_tab + "if err := LoadConfig(dirPath, fileName, obj.(proto.Message)); err != nil {" + base.change_line
        code += base.one_tab + base.one_tab + "return err, nil" + base.change_line
        code += base.one_tab + base.end_scope + base.change_line        
        code += base.empty_line
        code += base.one_tab +"return nil, obj.(proto.Message)" + base.change_line
        code += base.end_scope
        code += base.empty_line
        self.mCodeData += code

    def generate_new_cfg(self,class_name):
        class_name_cfg = class_name + "Cfg"
        code ="func" + base.one_space + "New" +class_name_cfg +"()" + base.one_space + "interface{}" + base.one_space + base.start_scope + base.change_line
        code += base.one_tab +"return" + base.one_space + "&"+class_name_cfg +"{}" + base.change_line
        code += base.end_scope + base.change_line
        code += base.empty_line 
        self.mCodeData += code

    def generate_register_all_cfg_start(self):        
        code ="func" + base.one_space + "RegisterAllExcelConfig()" + base.one_space + base.start_scope + base.change_line        
        self.mCodeData += code

    def generate_register_all_cfg_context(self,class_name):
        class_name_cfg = class_name + "Cfg"
        code = base.one_tab + "GStringToStructMgr.Register(\"" + class_name_cfg +"\","+ base.one_space + "New" + class_name_cfg + ")" + base.change_line
        self.mCodeData += code

    def generate_register_all_cfg_end(self):        
        code = base.end_scope + base.change_line
        code += base.change_line
        self.mCodeData += code        

    def generate_excel_cfg_reload_mgr(self):
        code = "type ExcelCfgReloadMgr struct {" + base.change_line
        code += base.one_tab + "funcs map[string]reflect.Value" + base.change_line
        code += base.end_scope + base.change_line
        code += base.empty_line
        code += "func NewExcelCfgReloadMgr() *ExcelCfgReloadMgr {" + base.change_line
        code += base.one_tab + "return &ExcelCfgReloadMgr{" + base.change_line
        code += base.one_tab + base.one_tab + "funcs: make(map[string]reflect.Value)," + base.change_line
        code += base.one_tab + base.end_scope + base.change_line 
        code += base.end_scope + base.change_line 
        code += base.empty_line
        code += "func (r *ExcelCfgReloadMgr) Init(x interface{}) {" + base.change_line
        code += base.one_tab + "RegisterAllExcelConfig()" + base.change_line
        code += base.one_tab + "t := reflect.TypeOf(x)" + base.change_line
        code += base.one_tab + "v := reflect.ValueOf(x)" + base.change_line
        code += base.one_tab + "for i := 0; i < t.NumMethod(); i++ {" + base.change_line 
        code += base.one_tab + base.one_tab + "methodName := t.Method(i).Name" + base.change_line 
        code += base.one_tab + base.one_tab + "r.funcs[methodName] = v.MethodByName(methodName)" + base.change_line
        code += base.one_tab + base.end_scope + base.change_line 
        code += base.end_scope + base.change_line
        code += base.empty_line 
        code += "func (r *ExcelCfgReloadMgr) Call(methodName string, message proto.Message) error {" +base.change_line
        code += base.one_tab + "if info, ok := r.funcs[methodName]; ok {" + base.change_line
        code += base.one_tab + base.one_tab + "info.Call([]reflect.Value{reflect.ValueOf(message)})" + base.change_line
        code += base.one_tab + base.one_tab + "return nil" + base.change_line
        code += base.one_tab + base.end_scope + base.change_line
        code += base.empty_line
        code += base.one_tab + "return fmt.Errorf(\"ExcelCfgReloadMgr Not Find MethodName: %v\", methodName)" + base.change_line
        code += base.end_scope + base.change_line 
        code += base.empty_line
        self.mCodeData += code     

    def generate_log(self):
        code = "type ILog interface " + base.start_scope + base.change_line 
        code += base.one_tab + "Debug(v ...interface{})" + base.change_line 
        code += base.one_tab + "Debugf(format string, v ...interface{})" + base.change_line
        code += base.empty_line
        code += base.one_tab + "Info(v ...interface{})" + base.change_line
        code += base.one_tab + "Infof(format string, v ...interface{})" + base.change_line
        code += base.empty_line
        code += base.one_tab + "Warn(v ...interface{})" + base.change_line
        code += base.one_tab + "Warnf(format string, v ...interface{})" + base.change_line
        code += base.empty_line
        code += base.one_tab + "Error(v ...interface{})" + base.change_line
        code += base.one_tab + "Errorf(format string, v ...interface{})" + base.change_line
        code += base.end_scope 
        code += base.empty_line
        self.mCodeData += code

    def generate_global_var(self):
        code = base.empty_line
        code += "var GConfigMgr *ConfigMgr" + base.change_line
        code += "var GExcelCfgReloadMgr *ExcelCfgReloadMgr" + base.change_line
        #code += "var ELog ILog" + base.change_line
        code += base.empty_line
        code += "func init() {" + base.change_line
        code += base.one_tab + "GConfigMgr = &ConfigMgr{}" + base.change_line
        code += base.one_tab + "GExcelCfgReloadMgr = NewExcelCfgReloadMgr()" + base.change_line
        code += "}" + base.change_line
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
    tool.generate_package()

    tool.generate_import()

    tool.generate_start_struct()    
    for classname in classnames:                                                        
        tool.generate_context_struct(classname)                
    tool.generate_end_struct()
    
    tool.generate_load_all_cfg_start()
    
    for classname in classnames:        
        tool.generate_load_all_cfg_context_new_obj(classname)

    tool.generate_load_all_cfg_context_map_start()
    for classname in classnames:  
        tool.generate_load_all_cfg_context_map_middle(classname)
    tool.generate_load_all_cfg_context_map_end()

    tool.generate_load_all_cfg_context_end()
    tool.generate_load_all_cfg_end()

    #id
    for classname in classnames:                
      tool.generate_get_by_id(classname)

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
        tool.generate_set_cfg(classname)
    
    tool.generate_load_cfg()
    tool.generate_reload_cfg()

    for classname in classnames:
        tool.generate_new_cfg(classname)

    tool.generate_register_all_cfg_start()
    for classname in classnames:
        tool.generate_register_all_cfg_context(classname)
    tool.generate_register_all_cfg_end()

    tool.generate_excel_cfg_reload_mgr()

    #tool.generate_log()
    tool.generate_global_var()    
    all_path_file_name = CFG_MGR_PATH + "/" + "configmgr.go"
    with open(all_path_file_name, 'wb') as data_file:
        data_file.write(''.join(tool.get_code_data()))    
    print "configmgr.go ok"


if __name__ == '__main__':
    Start()
