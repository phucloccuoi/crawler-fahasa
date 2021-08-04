from re import compile, sub

# Hàm chia nhỏ chuỗi lớn thành các chuỗi con
def split_big_str(input_string, str_slit, num_sub_str, remove_newline):
    '''
    Function: chia nhỏ chuỗi lớn thành các chuỗi con và cho vào dánh sách
    - str_slit: chuỗi phân cách giữa các chuỗi con
    - num_sub_str: số thứ tự
    - input_string: chuỗi đầu vào cần được chia nhỏ
    Return: hàm trả về danh sách các chuỗi con
    '''
    # Tách các chuỗi thành chuỗi con khi gặp chuỗi nhận dạng thành num_sub_str
    list_sub_string = input_string.split(str_slit, num_sub_str)

    # Xóa ký tự xuống dòng trong string
    if remove_newline == 1:
        temp = list_sub_string[num_sub_str]
        temp = temp.rstrip("\n")
        list_sub_string[num_sub_str] = temp

    return list_sub_string
# Kết thúc hàm chia nhỏ chuỗi lớn thành các chuỗi con

# Hàm thay thế các chuỗi thẻ html
def repalce_str_html(html_string, find_string, change_string):
    '''
    - Chức năng: xóa các chuỗi thẻ html không cần thiết
    - cleantext: Trả về ký tự khoảng trống cho chuỗi đầu vào
    '''
    # Tìm các thẻ <>
    cleanr = compile(find_string)

    # Xóa các thẻ <> chỉ chừa lại text
    cleantext = sub(cleanr, change_string, html_string)

    return cleantext
# Kết thúc hàm thay thế các chuỗi thẻ html

# Hàm xóa chuỗi thừa
def delete_str_unnecessary(html_string, list_str_del):
    '''
    Function: Xóa các thuộc tính, thẻ không cần thiết
    - html_string: chuỗi cần xử lý
    Return về chuỗi khi đã xóa
    '''
    # Khai báo biến chuỗi tạm thời & số chuỗi cần xóa
    temp_string = ''
    numFind_black = len(list_str_del)

    # Xóa các ký tự không cần thiết trong black_list
    for numfind in range(0, numFind_black):
        temp_string = str(html_string)
        html_string = ''
        html_string = repalce_str_html(temp_string, list_str_del[numfind], '')
    
    return html_string
# Kết quả hàm xóa chuỗi thừa

# Hàm thêm chuỗi từ danh sách
def add_str_description(html_string, list_str_change, list_str_changed):
    '''
    Function: Thêm và chỉnh sửa các thuộc tính của chuỗi HTML
    - html_string: chuỗi cần xử lý
    Return về chuỗi khi đã thêm các thuộc tính
    '''
    # Khai báo biến chuỗi tạm thời & số chuỗi cần thêm
    temp_string = ''
    numFind_change = len(list_str_change)
    
    # Thay đổi các ký tự trong change_list thành changed_list
    for numfind in range(0, numFind_change):
        temp_string = str(html_string)
        html_string = ''
        html_string = repalce_str_html(temp_string, list_str_change[numfind], list_str_changed[numfind])

    return html_string
# Kết quả hàm thêm chuỗi từ danh sách

# Hàm chỉnh sửa mô tả theo định dạng người dùng
def format_description(list_desc_full, name_product):
    '''
    Function: Định dạng lại các thẻ trong html như mong muốn
    - html_string: chuỗi cần xử lý và trả về chuỗi đã định dạng
    - name_product: tên sản phẩm
    Return về chuỗi có dịnh dạng ngon lành
    '''
    # Danh sách các chuỗi sẽ xóa
    black_list = ['\sclass="[a-z _-]+?"', '<(\/)?col.*?>', '<(\/)?div.*>', 'style=".*?"']

    # Danh sách cac chuỗi sẽ thay đổi
    change_list = ['href="+(.*)?"', 'F39801', '<th>']
    changed_list = ['href="https://www.fabico.vn/"', 'f35a01', '<th style="text-align: left;">']

    # Gọi các hàm thêm xóa mô tả
    str_desc = str(list_desc_full[0] + list_desc_full[1])
    str_desc = str(delete_str_unnecessary(str_desc, black_list))
    str_desc = str(add_str_description(str_desc, change_list, changed_list))

    # Tách thành các chuỗi con
    list_description = split_big_str(str_desc, "</table>", 1, 0)

    # Định dạng heading cho tên sản phẩm
    name_h2 = "<h2>" + name_product + "</h2>\n"
    name_h3 = "<h3>" + name_product + "</h3>\n"

    # Thêm định dạng các thẻ theo định dạng
    list_description[0] = name_h2 + "<div>" + list_description[0] + "</table>" + "</div>"
    list_description[1] = "<hr/>" + name_h3 + list_description[1]

    return str(list_description[0] + list_description[1])
# Kết thúc hàm chỉnh sửa mô tả theo định dạng người dùng

# Hàm định dạng mô tả cho trường SEO
def get_description_SEO(desc_SEO, name_product):
    '''
    Function: Định dạng lại phần mô tả SEO
    - html_string: chuỗi cần xử lý và trả về chuỗi đã định dạng
    Return về chuỗi có dịnh dạng ngon lành
    '''
    # Gọi hàm xóa các tag
    desc_SEO = repalce_str_html(desc_SEO, '<.*?>', '')

    # Danh sách các từ khóa cần chuyển đổi
    letters_Markups = ['&Agrave;', '&Egrave;', '&Igrave;', '&Ograve;', '&Ugrave;', '&agrave;', '&egrave;', '&igrave;', '&ograve;', '&ugrave;',
    '&Aacute;', '&Eacute;', '&Iacute;', '&Oacute;', '&Uacute;', '&Yacute;', '&aacute;', '&eacute;', '&iacute;', '&oacute;', '&uacute;', '&yacute;',
    '&Acirc;', '&Ecirc;', '&Ocirc;', '&acirc;', '&ecirc;', '&ocirc;', '&Atilde;', '&Otilde;', '&atilde;', '&otilde;', '&nbsp;']
    # Danh sách các từ khóa sẽ thay thế
    letters_Accents = ['À', 'È', 'Ì', 'Ò', 'Ù', 'à', 'è', 'ì', 'ò', 'ù',
    'Á', 'É', 'Í', 'Ó', 'Ú', 'Ý', 'á', 'é', 'í', 'ó', 'ú', 'ý',
    'Â', 'Ê', 'Ô', 'â', 'ê', 'ô', 'Ã', 'Õ', 'ã', 'õ', ' ']

    desc_SEO = str(add_str_description(desc_SEO, letters_Markups, letters_Accents))
    desc_SEO = " ".join(desc_SEO.split())
    
    return desc_SEO
# Kết thúc hàm định dạng mô tả cho trường SEO