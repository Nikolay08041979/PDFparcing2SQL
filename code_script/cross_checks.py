from pdffiletotext import get_paragraphperlist, get_paragraphperlist_slaver, get_paragraphperlist_master


def check_paragraph_number(): # choose all or chapter_number
    paragraphperlist = get_paragraphperlist()
    paragraphperlist_checklist = []
    for paragraph in paragraphperlist:
        paragraphperlist_checklist.append(paragraph[0])
    paragraph_check = paragraphperlist_checklist[1:]
    counter = 0
    for item in paragraph_check:
        item = item.split('.')
        if item[0] == '5' and (item[1] == '2' or item[1] == '3'):
            counter += 1
        else:
            counter += 0
    result_check = round(((counter/len(paragraph_check)) * 100))
    if result_check == 100:
        result = paragraph_check
        backupfile_path = 'backup_files/paragraph_check.txt'
        with open(backupfile_path, 'w') as f:
            for item in result:
                f.write(item + '\n')

        backupfile_path = './backup_files/paragraph_check_slave.txt'
        with open(backupfile_path, 'w') as f:
            for item in result:
                if item.split('.')[1] == '2':
                    f.write(item + '\n')

        backupfile_path = './backup_files/paragraph_check_master.txt'
        with open(backupfile_path, 'w') as f:
            for item in result:
                if item.split('.')[1] == '3':
                    f.write(item + '\n')

    return f'Всего в списке {len(paragraph_check)} параграфов. Из них {result_check}% прошли проверку \n' \
           f'Список параграфов доступен в папке backup_files.'

def get_paragraph_list_chapter(chapter_number): # 5.3 or 5.2
    paragraph_list = []
    with open('./backup_files/paragraph_check.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            paragraph_list.append(line)
    if chapter_number not in '5.3.001':
        last_page_slave = paragraph_list.index('5.3.001')
        paragraph_list = paragraph_list[:last_page_slave]
    else:
        first_page_master = paragraph_list.index('5.3.001')
        paragraph_list = paragraph_list[first_page_master:]
    return paragraph_list

#
def get_pgn_status():
    slave_list = get_paragraphperlist_slaver()
    counter1 = 0
    counter2 = 0
    for paragraph in slave_list:
        for i, elem in enumerate(paragraph):
            if elem == "PGN":
                print(f'{counter1}) параграф: {paragraph[0]}, PGN: {elem}, index: {i}, value: {paragraph[i+2]}')
                counter1 += 1
            else:
                counter2 += 1
    return f"Обработано {counter1 + counter2} параграфов из {len(slave_list)}: \n" \
           f"1) найдено {counter1} параграфов с PGN. \n" \
           f"2) пропущено {counter2} параграфов без PGN. "
#


def get_paragrapth_text(parag_nunber, textnextelement=None):
    paragraph_number = parag_nunber.split('.')
    if paragraph_number[1] == '2':
        for paragraph in get_paragraphperlist_slaver():
            if paragraph[0] == parag_nunber:
                return paragraph
    else:
        for paragraph in get_paragraphperlist_master():
            if paragraph[0] == parag_nunber:
                if paragraph[0] != '5.3.2??':
                    return paragraph
                else:
                    if paragraph[1] == textnextelement:
                        return paragraph


#print(check_paragraph_number())
#print(get_params_slave_chapter())
#print(check_dataframe_vs_sql_qty_strings())
#print(get_paragraph_list_chapter('5.2'))
#print(check_pgn_slave_chapter())
#print(get_pgn_status())
#print(get_paragrapth_text('5.3.145'))