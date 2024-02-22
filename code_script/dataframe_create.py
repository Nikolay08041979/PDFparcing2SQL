import pandas as pd
import json
from pdffiletotext import get_paragraphperlist_slaver, get_paragraphperlist_master

def get_slot_scaling(spn_doc, parameter_group): # parameter_name - ? to increase accuracy
    paragraphperlist_slaver = get_paragraphperlist_slaver()
    for paragraph in paragraphperlist_slaver:
        for item in paragraph:
            if paragraph[0] == spn_doc:
                if paragraph[paragraph.index('PGN') + 2] == parameter_group:
                    if "Slot Scaling" in item:
                        slot_scaling_index = paragraph.index(item)
                        slot_scaling_value = (paragraph[(slot_scaling_index)].split('Scaling')[1]).lstrip()
                        return slot_scaling_value
                    else:
                        continue

def get_spn(spn_doc, parameter_group): # parameter_name - ? to increase accuracy
    paragraphperlist_slaver = get_paragraphperlist_slaver()
    for paragraph in paragraphperlist_slaver:
        for item in paragraph:
            if paragraph[0] == spn_doc:
                if paragraph[paragraph.index('PGN') + 2] == parameter_group:
                    if "SPN" == item:
                        spn_index = paragraph.index(item) + 1
                        spn_value = paragraph[(spn_index)]
                        return spn_value
                    else:
                        continue

def get_slot_range(spn_doc, parameter_group): # parameter_name - ? to increase accuracy
    paragraphperlist_slaver = get_paragraphperlist_slaver()
    for paragraph in paragraphperlist_slaver:
        for item in paragraph:
            if paragraph[0] == spn_doc:
                if paragraph[paragraph.index('PGN') + 2] == parameter_group:
                    if "Slot Range" in item:
                        slot_range_index = paragraph.index(item) + 1
                        slot_range_value = paragraph[(slot_range_index)]
                        return slot_range_value
                    else:
                        continue

def get_datadict_for_dataframe_master():
    data_set_template = ['SPN Doc', 'Date', 'POS', 'Length', 'Parameter Name', 'SPN']
    data_dict = []
    paragraphperlist_master = get_paragraphperlist_master()
    for i, paragraph in enumerate(paragraphperlist_master):
        param_spisok = int(((len(paragraph) - (paragraph.index('SPN Doc'))) / len(data_set_template)))
        for k in range(param_spisok - 1):
            parameter_group_value = paragraph[(paragraph.index('Parameter Group')) + 1]
            spn_doc_value = paragraph[(((paragraph.index('SPN Doc')) + 4) + len(data_set_template)) + (len(data_set_template) * k)]
            data_set_str = {'MPRGR': paragraph[0],
                            'ID': paragraph[(paragraph.index('Parameter Group')) + 2],
                            'PGN': parameter_group_value,
                            'Data_Length': paragraph[(paragraph.index('Data Length')) + 1],
                            'Length': ((((paragraph.index('SPN Doc')) + 1) + len(data_set_template)) + (len(data_set_template) * k)),
                            '_Name_': paragraph[(((paragraph.index('SPN Doc')) + 2) + len(data_set_template)) + (len(data_set_template) * k)],
                            'SPN Doc': spn_doc_value}
            data_dict.append(data_set_str)
    return data_dict

def get_json_from_data_dict():
    data_dict_list = get_datadict_for_dataframe_master()
    with open('backup_files/data_master_file.json', 'w') as file:
        json_data = file.write(json.dumps(data_dict_list, indent=4))
    return json_data

def update_json_slave_param(): #which param would you like to update
    with open('backup_files/data_master_file.json', 'r') as file:
        data = json.load(file)
        for i in range(len(data)):
            data[i]['Scaling'] = get_slot_scaling(data[i]['SPN Doc'], data[i]['PGN'])
            data[i]['_Range_'] = get_slot_range(data[i]['SPN Doc'], data[i]['PGN'])
            data[i]['SPN'] = get_spn(data[i]['SPN Doc'], data[i]['PGN'])
            with open('backup_files/data_master_file.json', 'w') as file:
                json.dump(data, file, indent=4)
        return

def get_json_print_none(): # put a param on which need to prove the list
    counter = 0
    with open('backup_files/data_master_file.json', 'r') as file:
        data = json.load(file)
        for i in range(len(data)):
            if data[i]['Scaling'] is None or data[i]['_Range_'] is None or data[i]['SPN'] is None:
                print(data[i])
                counter += 1
        return f'Всего повреждено {counter} строк из {len(data)}, что составляет {round((counter / len(data) * 100),2)}%'


def get_json_update_none_only():
    with open('backup_files/data_master_file.json', 'r') as file:
        data = json.load(file)
        for i in range(len(data)):
            if data[i]['Scaling'] is None or data[i]['_Range_'] is None or data[i]['SPN'] is None:
                data[i]['Scaling'] = get_slot_scaling(data[i]['SPN Doc'], data[i]['PGN'])
                data[i]['_Range_'] = get_slot_range(data[i]['SPN Doc'], data[i]['PGN'])
                data[i]['SPN'] = get_spn(data[i]['SPN Doc'], data[i]['PGN'])
                with open('backup_files/data_master_file.json', 'w') as file:
                    json.dump(data, file, indent=4)
        return

def get_data_frame_from_json():
    col = ['ID', 'Data_Length', 'Length', '_Name_', 'Scaling', '_Range_', 'SPN']
    with open('backup_files/data_master_file.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    dataframe_pdf = pd.DataFrame(data, columns=col)
    return dataframe_pdf

#print(get_spn('5.2.1.09', '61444'))
#print(get_slot_range('5.2.1.09', '61444'))
#print(get_slot_scaling('5.2.5.286', '65130'))
#print(get_datadict_for_dataframe())
#print(get_json_from_data_dict())
#print(update_json_slave_param())
#print(get_json_update_none_only())
#print(get_data_frame_from_json())
#print(get_json_print_none())



