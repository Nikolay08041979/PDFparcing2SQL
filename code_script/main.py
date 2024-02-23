from code_script.dataframe_create import get_json_print_none
from dataframe_export import export_dataframe_to_sql, get_count_sql
#from code_script.dataframe_create import get_data_frame_from_json

def samarry():
    get_json_print_none()
    export_dataframe_to_sql()
    get_count_sql()
    return

if __name__ == '__main__':
    print(samarry())

