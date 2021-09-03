#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import sys
import xlrd
import string
import shutil 
import base

EXCEL_PATH = sys.argv[1]
PROTO_CACHE_PATH = sys.argv[2]
PYTHON_CACHE_PATH = sys.argv[3]
CLASSNAME_CACHE_PATH = sys.argv[4]

#EXCEL_PATH = u"./excel"
#PROTO_CACHE_PATH = u"./cache/proto"
#PYTHON_CACHE_PATH = u"./cache/python"
#CLASSNAME_CACHE_PATH = u"./cache/classname"


class CTool:
    def __init__(self):        
        self.mCodeData = []

    def get_code_data(self):
        return self.mCodeData    

    def read(self,file_full_path,filename):                    
        xlsxfile = xlrd.open_workbook(file_full_path)
        sheet_names = xlsxfile.sheet_names()
        print sheet_names
        is_need_write = False 
        header_flag = True 
        for index in range (0,len(sheet_names)):
            table = xlsxfile.sheet_by_index(index)
            proto_name = filename +  sheet_names[index].capitalize() 
            row_num = table.nrows     # 行
            col_num = table.ncols     # 列            
            if row_num <= base.data_start_row:
                continue
            #是否含有server字段
            has_s_flag = False              
            for j in range(0, col_num):
                cs_flag = table.cell_value(base.cs_row, j)
                if base.is_server(cs_flag) or base.is_client_and_server(cs_flag):
                    has_s_flag = True
                    break
            if has_s_flag == False:
                continue
            classname_file_name = CLASSNAME_CACHE_PATH + "/classname.txt"
            with open(classname_file_name, 'a+') as data_file:  
                classname_data = proto_name + base.one_space           
                data_file.write(''.join(classname_data))

            english_names = []                
            server_types = []                                                                          
            for j in range(0, col_num):     
                server_type = table.cell_value(base.server_type_row, j)
                if base.check_data_type(server_type):
                    cs_flag = table.cell_value(base.cs_row, j)
                    if base.is_server(cs_flag) or base.is_client_and_server(cs_flag):                           
                        english_name = table.cell_value(base.english_row, j)
                        server_types.append(server_type)
                        english_names.append(english_name)               
                else:
                    print "read", filename, server_type," col=", j, " server_type error"
            if header_flag == True:
                self.proto3_generate()
                header_flag = False 
            self.proto_generate(proto_name, english_names, server_types)
            self.proto_list_generate(proto_name)
            is_need_write = True 
        return True,is_need_write

    def proto3_generate(self):
        code = "syntax = " + "\"proto3\"" + base.semicolon + base.change_line             
        code += "package" + base.one_space + "config;" + base.change_line
        self.mCodeData += code

    def proto_generate(self, classname, names, types):        
        code = base.empty_line
        code += "message" + base.one_space + classname + base.change_line
        code += base.start_scope + base.change_line

        line_num = 1

        for j in range(0, len(types)):
            if base.is_base(types[j]):
                field_code = base.one_tab + types[j] + base.one_space + names[j] + base.one_space + base.equal_symbol + base.one_space + str(line_num) + base.semicolon + base.change_line
                code += field_code
            elif  base.is_array(types[j]):
                field_code = base.one_tab + "repeated" + base.one_space + base.get_array_type(types[j]) + base.one_space + names[j] + base.one_space + base.equal_symbol + base.one_space + str(line_num) + base.semicolon + base.change_line
                code += field_code
            elif base.is_map(types[j]):
                key_type,value_type = base.get_map_type(types[j])
                field_code = base.one_tab + "map<" + key_type + base.comma_symbol + value_type + ">" + base.one_space + names[j] + base.equal_symbol + base.one_space + str(line_num) + base.semicolon + base.change_line
                code += field_code
            else:
                print classname,types[j],"type error"
                sys.exit(1)
            line_num += 1            
        code += base.end_scope
        code += base.change_line
        self.mCodeData += code
        
    def proto_list_generate(self, classname):
        code = base.change_line
        code += "message" + base.one_space + classname + "Cfg" + base.change_line
        code += base.start_scope + base.change_line
        line_num = 1        
        code += base.one_tab + "map<uint32," + classname + ">" + base.one_space + "datas" + base.equal_symbol + base.one_space + str(line_num) + base.semicolon + base.change_line        
        code += base.end_scope
        code += base.change_line
        self.mCodeData += code

    
def Start():        
    if os.path.exists(PROTO_CACHE_PATH): shutil.rmtree(PROTO_CACHE_PATH)    
    if not os.path.exists(PROTO_CACHE_PATH): os.makedirs(PROTO_CACHE_PATH)
    if os.path.exists(PYTHON_CACHE_PATH): shutil.rmtree(PYTHON_CACHE_PATH)
    if not os.path.exists(PYTHON_CACHE_PATH): os.makedirs(PYTHON_CACHE_PATH)
    if os.path.exists(CLASSNAME_CACHE_PATH): shutil.rmtree(CLASSNAME_CACHE_PATH)
    if not os.path.exists(CLASSNAME_CACHE_PATH): os.makedirs(CLASSNAME_CACHE_PATH)
    
    for root, dirs, files in os.walk(EXCEL_PATH):
        for filename in files:
            file_full_path = os.path.join(EXCEL_PATH, filename)
            if os.path.exists(file_full_path):                                                
                file_name = filename.replace(".xlsx", "")
                cap_file_name = file_name.capitalize()
                try:
                    tool = CTool()
                    success = tool.read(file_full_path,cap_file_name)
                except Exception, e:
                    print "tool read err:",e 
                    sys.exit(1)
                if (success[0] == True) and (success[1] == True):                                                  
                    all_path_file_name = PROTO_CACHE_PATH + "/" + file_name + ".proto"      
                    with open(all_path_file_name, 'wb') as data_file:
                        data_file.write(''.join(tool.get_code_data()))                    
            else:
                print root, dirs, filename, " don't exist"


if __name__ == '__main__':
    Start()
