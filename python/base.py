import sys
import string

#Common Characters
change_line = "\n"
empty_line = "\n"
one_space = " "
start_scope = "{" + one_space
end_scope = "}" + one_space
one_tab = "    "
two_tab= "        "
semicolon = ";"
equal_symbol = "="
comma_symbol = ","

#Data Type
base_data_type = ("bool","int32","uint32","int64","uint64","string","float","double")
array_data_type = ("int32[]","uint32[]","int64[]","uint64[]","string[]")
map_data_key_type= ("int32","uint32","int64","uint64","string")
map_data_value_type= ("int32","uint32","int64","uint64","string")

english_row = 1
cs_row = 2
server_type_row = 4
limit_row = 5
data_start_row = 8

def check_data_type(field_name):
    return  is_base(field_name) or is_array(field_name) or is_map(field_name)

def get_handle_string(src):
    return src.replace('\n', '').replace('\r', '').replace(' ', '')

def is_base(field_name):
    field_name = get_handle_string(field_name)
    return (field_name in base_data_type)

def is_array(field_name):
    field_name = get_handle_string(field_name)
    return (field_name in array_data_type)

def get_array_type(field_name):
    field_name = get_handle_string(field_name)
    field_name = field_name.replace('[', '')
    field_name = field_name.replace(']', '')
    return field_name

def is_map(field_name):
    field_name = get_handle_string(field_name)    
    if field_name.find("[") == -1:
        return False 
    if field_name.find("=") == -1:
        return False 
    if field_name.find("]") == -1:
        return False 
    field_name = field_name.replace('[', '')
    field_name = field_name.replace(']', '')
    
    map_types = field_name.split("=")
    if len(map_types) != 2:
        return False
    if (map_types[0] in map_data_key_type) == False:
        return False
    if (map_types[1] in map_data_value_type) == False:
        return False

    return True

def get_map_type(field_name):
    field_name = get_handle_string(field_name)    
    field_name = field_name.replace('[', '')
    field_name = field_name.replace(']', '')    
    map_types = field_name.split("=")    
    return map_types[0],map_types[1]

def is_server(field_name):
    field_name = get_handle_string(field_name)
    return field_name.find("S") 

def is_client(field_name):
    field_name = get_handle_string(field_name)
    return field_name.find("C")

def is_limit(field_name):
    if field_name =="":
        return False,0,0
    field_name = get_handle_string(field_name)
    if field_name.find("-") == -1:
        return False,0,0
    limits = field_name.split("-")
    if len(limits) != 2:
        return False,0,0
    return True,int(limits[0]),int(limits[1])

def is_client_and_server(field_name):
    field_name = get_handle_string(field_name)
    return field_name.find("CS")

def import_mod(path,modname):
    if sys.modules.has_key(modname): del sys.modules[modname]
    sys.path.insert(0, path)
    mod = __import__(modname)
    del sys.path[0]
    return mod

def parse_value(type_name,val):
    if type_name == "bool": 
        if val == "": val = "0"
        return int(val) != 0
    elif type_name == "float":
        if val == "": val = "0.0"
        return float(val)
    elif type_name == "double":
        if val == "": val = "0.0"
        return float(val)
    elif type_name == "string":
        return str(val).strip().decode("UTF-8")    
    else:
        if val == "": val = "0"
        return int(float(val))

def main():
    pass

if __name__ == '__main__':
    main()