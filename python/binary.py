#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import sys
import os
import imp
import re
import string
import shutil 
import base

#EXCEL_PATH = sys.argv[1]
#PYTHON_CACHE_PATH = sys.argv[2]
#BINARY_CACHE_PATH = sys.argv[3]

EXCEL_PATH = u"./excel"
PYTHON_CACHE_PATH = u"./cache/python/"
BINARY_CACHE_PATH = u"./cache/binary/"

class CTool:
    def parse(self,file_full_path,filename):
        cap_file_name = filename.capitalize()
        xlsxfile = xlrd.open_workbook(file_full_path)
        sheet_names = xlsxfile.sheet_names()
        #print sheet_names           
        mod = base.import_mod(PYTHON_CACHE_PATH,filename + "_pb2")     
        for index in range (0,len(sheet_names)):
            table = xlsxfile.sheet_by_index(index)            
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
            
            class_cfg_name = cap_file_name +  sheet_names[index].capitalize() +"Cfg"      
            cfg_obj = eval("mod." + class_cfg_name + "()")                                       
            for i in range(base.data_start_row, row_num):
                id_cell = table.cell(i, 0)
                id = int(id_cell.value)                         
                obj = cfg_obj.datas[id]
                for j in range(0, col_num):
                    cs_flag = table.cell_value(base.cs_row, j)
                    if base.is_server(cs_flag) or base.is_client_and_server(cs_flag):  
                        cell = table.cell(i, j)
                        english_name = table.cell_value(base.english_row, j)
                        server_type = table.cell_value(base.server_type_row, j)                        
                        if hasattr(obj, english_name):
                            val = str(cell.value)
                            if base.is_base(server_type):  
                                val = base.parse_value(server_type,val)
                                setattr(obj,english_name,base.parse_value(server_type,val))

                                limit_flag,min_val,max_val = base.is_limit(table.cell_value(base.limit_row,j))
                                if limit_flag == True: 
                                    if (val < min_val) or (val > max_val):
                                        print filename,sheet_names[index],(i,j),val,"not in",min_val,max_val,"error"
                                        sys.exit(1)                                
                            elif base.is_array(server_type):                                
                                if val != '':
                                    strs = re.split('[| ,;:]',val)
                                    var = getattr(obj,english_name)
                                    array_type = base.get_array_type(server_type)
                                    for s in strs:                                        
                                        var.append(base.parse_value(array_type,s))
                            elif base.is_map(server_type): 
                                val = str(val)
                                if val !='' and val != '0' and val != '0.0':
                                    strs = re.split('[| ,;:]', val)
                                    for s in strs:
                                        var = getattr(obj, english_name)
                                        key_type,val_type = base.get_map_type(server_type)
                                        group = re.split('=',s)
                                        mkey = base.parse_value(key_type, group[0])
                                        mval = base.parse_value(val_type, group[1])
                                        var[mkey] = mval
                            else:
                                print filename,sheet_names[index],(i,j),"server_type error"
                                sys.exit(1)

            PbName = BINARY_CACHE_PATH + cap_file_name +  sheet_names[index].capitalize() + ".pb"
            #print PbName
            with open(PbName, 'wb') as dataFile:
                dataFile.write(cfg_obj.SerializeToString())

def Start():        
    if os.path.exists(BINARY_CACHE_PATH): shutil.rmtree(BINARY_CACHE_PATH)    
    if not os.path.exists(BINARY_CACHE_PATH): os.makedirs(BINARY_CACHE_PATH)
    
    for root, dirs, files in os.walk(EXCEL_PATH):
        for filename in files:
            array = filename.split(".")
            if len(array) < 2:
                continue
            if array[1] != "xlsx":
                continue

            file_full_path = os.path.join(EXCEL_PATH, filename)
            if os.path.exists(file_full_path):                                                
                file_name = filename.replace(".xlsx", "")                
                try:
                    tool = CTool()
                    tool.parse(file_full_path,file_name)
                except Exception, e:
                    print "tool parse err:",e
                    sys.exit(1)                
            else:
                print root, dirs, filename, " don't exist"           

if __name__ == '__main__':
    Start()