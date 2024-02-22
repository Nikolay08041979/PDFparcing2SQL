import fitz

pdf_file_name_path = '../pdf_files/SAE_J1939-71.pdf'
master_chapter_start_page = 332  # 5.3 is the master chapter and 5.2 slave chapter


def transform_pdf_file_to_onetextpageperlist():  # exapmle: 'SAE_J1939-71.pdf' location: ./SAE_J1939-71.pdf (the same folder where the script is located)
    pdf_file_name = fitz.open(pdf_file_name_path)
    textpageperlist = []
    for page in range(pdf_file_name.page_count):
        page_data = pdf_file_name.load_page(page)
        page_text = (page_data.get_text()).split(' \n')
        for i in range(len(page_text)):  # text cleaning:remove empty strings, brackets, spaces and ':'
            page_text[i] = ' '.join(page_text[i].split(')'))
            page_text[i] = ' '.join(page_text[i].split('('))
            page_text[i] = page_text[i].replace(':', '')
            page_text[i] = page_text[i].replace('and paragraph Approved', '')
            page_text[i] = ' '.join(page_text[i].split())
        page_text = [i for i in page_text if i]  # remove empty strings
        textpageperlist.append(page_text)  # each page is a list
    return textpageperlist


def get_text_to_onelist_nopagenum():
    textpageperlist = transform_pdf_file_to_onetextpageperlist()
    for page in textpageperlist:  # remove page number and 2 next elements from master_list
        page.pop(0)
        page.pop(0)
        page.pop(0)
    textonelist_nopagenum = [name for page in textpageperlist for name in page]  # join all pages onto one list
    return textonelist_nopagenum


def get_text_to_onelist_nopagenum_master():
    textpageperlist = transform_pdf_file_to_onetextpageperlist()
    textpageperlist_master = textpageperlist[(master_chapter_start_page - 1):]
    for page in textpageperlist_master:  # remove page number and 2 next elements from master_list
        page.pop(0)
        page.pop(0)
        page.pop(0)
    textonelist_nopagenum_master = [name for page in textpageperlist_master for name in
                                    page]  # join all pages onto one list
    return textonelist_nopagenum_master


def get_text_to_onelist_nopagenum_slaver():
    textpageperlist = transform_pdf_file_to_onetextpageperlist()
    textpageperlist_slaver = textpageperlist[:master_chapter_start_page]
    for page in textpageperlist_slaver:  # remove page number and 2 next elements from master_list
        page.pop(0)
        page.pop(0)
        page.pop(0)
    textonelist_nopagenum_slaver = [name for page in textpageperlist_slaver for name in
                                    page]  # join all pages onto one list
    return textonelist_nopagenum_slaver


def get_paragraphperlist():
    textonelist_nopagenum = get_text_to_onelist_nopagenum()
    paragraphperlist_nopagenum = [[]]
    for item in textonelist_nopagenum:
        if item == '-71':
            paragraphperlist_nopagenum.append([])
        else:
            paragraphperlist_nopagenum[-1].append(item)
    return paragraphperlist_nopagenum


def get_paragraphperlist_master():
    textonelist_nopagenum_master = get_text_to_onelist_nopagenum_master()
    paragraphperlist_nopagenum_master = [[]]
    for item in textonelist_nopagenum_master:
        if item == '-71':
            paragraphperlist_nopagenum_master.append([])
        else:
            paragraphperlist_nopagenum_master[-1].append(item)
    paragraphperlist_master = [i for i in paragraphperlist_nopagenum_master if i]  # remove empty lists
    backup_podstroka = []
    for paragraph in paragraphperlist_master:
        for i, item in enumerate(paragraph):
            if paragraph[0] == '5.3.013':
                if item == '5.2.1.06':
                    for j in range(i + 1, len(paragraph)):
                        backup_podstroka.append(paragraph[j])
                    paragraph.insert(i + 1, '')  # empty string to add instead of missed date
                    paragraph.extend(backup_podstroka)

    for paragraph in paragraphperlist_master:
        for item in paragraph:
            if paragraph[0] == '5.3.015' or paragraph[0] == '5.3.017':
                if item == 'Configuration' or item == 'Engine Configuration' or item == 'Limit':
                    paragraph.remove(item)

    backup_podstroka1 = []
    backup_podstroka2 = []
    backup_podstroka3 = []
    for paragraph in paragraphperlist_master:
        for i, item in enumerate(paragraph):
            if paragraph[0] == '5.3.025':
                if item == '5.2.5.090':
                    for j in range(i + 3, len(paragraph)):
                        backup_podstroka1.append(paragraph[j])
                    for j in range(i + 3, len(paragraph)):
                        elem = paragraph.pop()
                        backup_podstroka2.append(elem)
    variabl_model = backup_podstroka2.pop()
    variabl_model_split = variabl_model.split()
    backup_podstroka3.append(variabl_model_split[0])
    backup_podstroka3.append(variabl_model_split[1])
    for i in range(3):
        backup_podstroka3.append(backup_podstroka2.pop())
    for i in range(6):
        backup_podstroka2.pop()
    backup_podstroka3.append(backup_podstroka2.pop())
    variabl_serial_number = backup_podstroka2.pop()
    vsn_split = variabl_serial_number.split()
    backup_podstroka3.append(vsn_split[0])
    sn = ' '.join(vsn_split[1:])
    backup_podstroka3.append(sn)
    for i in range(3):
        backup_podstroka3.append(backup_podstroka2.pop())
    for i in range(6):
        backup_podstroka2.pop()
    backup_podstroka3.append(backup_podstroka2.pop())
    variabl_unp = backup_podstroka2.pop()
    vunp_split = variabl_unp.split()
    backup_podstroka3.append(vunp_split[0])
    snp = ' '.join(vunp_split[1:])
    backup_podstroka3.append(snp)

    for i in range(3):
        backup_podstroka3.append(backup_podstroka2.pop())
    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.025':
            for elem in backup_podstroka3:
                paragraph.append(elem)
    backup_podstroka4 = []
    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.026':
            for i in range(6):
                paragraph.pop()
            for i in range(5):
                elem1 = paragraph.pop()
                backup_podstroka4.append(elem1)
            paragraph.append(backup_podstroka4.pop())

            variabl_vin = backup_podstroka4.pop()
            vvin_split = variabl_vin.split()
            paragraph.append(vvin_split[0])
            snp = ' '.join(vvin_split[1:])
            paragraph.append(snp)
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.029':
            for i in range(34):
                elem = paragraph.pop()
                backup_podstroka4.append(elem)
            elem1 = paragraph.pop() + ' ' + backup_podstroka4[-4]
            paragraph.append(elem1)
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
            for i in range(30):
                paragraph.append(backup_podstroka4.pop())
    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.030':
            for i in range(6):
                paragraph.pop()
            for i in range(5):
                elem1 = paragraph.pop()
                backup_podstroka4.append(elem1)
            paragraph.append(backup_podstroka4.pop())
            variabl_vin = backup_podstroka4.pop()
            vvin_split = variabl_vin.split()
            paragraph.append(vvin_split[0])
            snp = ' '.join(vvin_split[1:])
            paragraph.append(snp)
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())

            backup_podstroka4.extend(paragraph[75:])
            del paragraph[75:]
            elem = backup_podstroka4.pop(0) + ' ' + backup_podstroka4.pop(0)
            paragraph.append(elem)
            for elem in backup_podstroka4:
                paragraph.append(elem)

    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.076':
            for i in range(((paragraph.index('SPN')) + 3), len(paragraph)):
                elem = paragraph.pop()
                backup_podstroka4.append(elem)
            baphr = backup_podstroka4[-1] + ' ' + backup_podstroka4[-5]
            paragraph.append(baphr)
            backup_podstroka4.pop()
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
            paragraph.append(backup_podstroka4.pop())
            paragraph.append(backup_podstroka4.pop())
            baphr = backup_podstroka4[-1] + ' ' + backup_podstroka4[-5]
            paragraph.append(baphr)
            backup_podstroka4.pop()
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
            paragraph.append(backup_podstroka4.pop())
            paragraph.append(backup_podstroka4.pop())
            baphr = backup_podstroka4[-1] + ' ' + backup_podstroka4[-5]
            paragraph.append(baphr)
            backup_podstroka4.pop()
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
            paragraph.append(backup_podstroka4.pop())
            paragraph.append(backup_podstroka4.pop())
            baphr = backup_podstroka4[-1] + ' ' + backup_podstroka4[-5]
            paragraph.append(baphr)
            backup_podstroka4.pop()
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
            paragraph.append(backup_podstroka4.pop())
            paragraph.append(backup_podstroka4.pop())
            baphr = backup_podstroka4[-1] + ' ' + backup_podstroka4[-5]
            paragraph.append(baphr)
            backup_podstroka4.pop()
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
            paragraph.append(backup_podstroka4.pop())
            paragraph.append(backup_podstroka4.pop())
            baphr = backup_podstroka4[-1] + ' ' + backup_podstroka4[-5]
            paragraph.append(baphr)
            backup_podstroka4.pop()
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
            paragraph.append(backup_podstroka4.pop())
            paragraph.append(backup_podstroka4.pop())
            baphr = backup_podstroka4[-1] + ' ' + backup_podstroka4[-5]
            paragraph.append(baphr)
            backup_podstroka4.pop()
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
            paragraph.append(backup_podstroka4.pop())
            paragraph.append(backup_podstroka4.pop())
            baphr = backup_podstroka4[-1] + ' ' + backup_podstroka4[-5]
            paragraph.append(baphr)
            backup_podstroka4.pop()
            for i in range(3):
                paragraph.append(backup_podstroka4.pop())
            backup_podstroka4.pop()
    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.079':
            paragraph.pop(37)

    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.102':
            del paragraph[61:]
        if paragraph[0] == '5.3.110':
            paragraph.pop(paragraph.index('444'))

    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.145':
            for i in range(5):
                paragraph.pop()
            elem = paragraph.index('e')
            for i in range(5):
                paragraph.pop(elem)
            backup_podstroka4.clear()
            elem = paragraph.index('Variabl Driver 1 identification')
            paragraph.pop(paragraph.index('Variabl Driver 1 identification'))
            paragraph.pop(paragraph.index('Variabl Driver 2 identification'))
            backup_podstroka4.extend(paragraph[elem:])
            paragraph.append('Variabl')
            paragraph.append('Driver 1 identification')
            for elem in backup_podstroka4[:4]:
                paragraph.append(elem)
            paragraph.append('Variabl')
            paragraph.append('Driver 2 identification')
            for elem in backup_podstroka4[4:]:
                paragraph.append(elem)
            paragraph.pop(paragraph.index('5.2.5.287'))

    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.2??' and paragraph[1] == 'Continuous Torque & Speed Limit Request':
            del paragraph[74:]

    for paragraph in paragraphperlist_master:
        if paragraph[0] == '5.3.2??' and paragraph[1] == 'Retarder Continuous Torque & Speed Limit':
            paragraph.append('11/13/1999')
            for i in range(2):
                elem = paragraph.index('from Retarder')
                paragraph.pop(elem)
        if paragraph[0] == '5.3.2??' and paragraph[1] == 'Engine Continuous Torque & Speed Limit':
            elem = paragraph.index('from Engine')
            paragraph.pop(elem)
            elem = paragraph.index('RPM')
            paragraph.pop(elem)

    return paragraphperlist_master

def get_paragraph_list_chapter(chapter_number: str):  # 5.3 or 5.2
    paragraph_list = []
    if chapter_number == '5.3':
        with open('./backup_files/paragraph_check_master.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                paragraph_list.append(line)
    else:
        with open('./backup_files/paragraph_check_slave.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                paragraph_list.append(line)
    return paragraph_list


def get_paragraphperlist_slaver(chapter_number=None):
    textonelist_nopagenum_slaver = get_text_to_onelist_nopagenum_slaver()
    paragraphperlist_nopagenum_slaver = [[]]
    for item in textonelist_nopagenum_slaver:
        if item == '-71':
            paragraphperlist_nopagenum_slaver.append([])
        else:
            paragraphperlist_nopagenum_slaver[-1].append(item)
    for i, paragraph in enumerate(paragraphperlist_nopagenum_slaver):
        if paragraph[0] == '5.2.5.286':  # remove double lists where one is without PGN --> cross check pgn status
            del paragraphperlist_nopagenum_slaver[i]
    paragraphperlist_slaver = [i for i in paragraphperlist_nopagenum_slaver if i]  # remove empty lists
    return paragraphperlist_slaver


# print(transform_pdf_file_to_onetextpageperlist())
# print(get_text_to_onelist_nopagenum())
# print(get_text_to_onelist_nopagenum_master())
# print(get_text_to_onelist_nopagenum_slaver())
# print(get_paragraphperlist())
#print(get_paragraphperlist_master())
# print(get_paragraphperlist_slaver())
# print(convert_paragraphperlist_to_txt('5.3'))
# print(convert_paragraphperlist_to_txt('5.2'))
