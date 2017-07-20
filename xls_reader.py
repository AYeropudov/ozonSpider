import openpyxl as xl


def get_arts_from_xls():
    wb = xl.load_workbook(u"/home/alex/spider/xls/price.xlsx")
    sheet = wb.get_active_sheet()
    x = sheet['F']
    filtered_cells = []
    for cell in x:
        if cell.value is not None and cell.row != 3:
            filtered_cells.append((cell.value, cell.row))
    return filtered_cells


def put_stat_toxls(tuple_list):
    wb = xl.load_workbook(u"/home/alex/spider/xls/price.xlsx")
    sheet = wb.get_active_sheet()
    for tuple_data in tuple_list:
        sheet[u'{}{}'.format('R', tuple_data[0])] = tuple_data[1]
        sheet[u'{}{}'.format('S', tuple_data[0])] = tuple_data[2]
    wb.save(u"/home/alex/spider/xls/price_result.xlsx")
