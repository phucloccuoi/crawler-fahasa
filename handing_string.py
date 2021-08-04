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
def delete_str_unnecessary(html_string):
    '''
    Function: Xóa các thuộc tính, thẻ không cần thiết
    - html_string: chuỗi cần xử lý
    Return về chuỗi khi đã xóa
    '''
    # Danh sách các chuỗi sẽ xóa
    black_list = ['\sclass="[a-z _-]+?"', '<(\/)?col.*?>', '<(\/)?div.*>', 'style=".*?"']

    # Khai báo biến chuỗi tạm thời & số chuỗi cần xóa
    temp_string = ''
    numFind_black = len(black_list)

    # Xóa các ký tự không cần thiết trong black_list
    for numfind in range(0, numFind_black):
        temp_string = str(html_string)
        html_string = ''
        html_string = str(repalce_str_html(temp_string, black_list[numfind], ''))
    
    return html_string
# Kết quả hàm xóa chuỗi thừa

# Hàm thêm chuỗi
def add_str_description(html_string):
    '''
    Function: Thêm và chỉnh sửa các thuộc tính của chuỗi HTML
    - html_string: chuỗi cần xử lý
    Return về chuỗi khi đã thêm các thuộc tính
    '''
    # Danh sách cac chuỗi sẽ thay đổi
    change_list = ['href="+(.*)?"', 'F39801', '<th>']
    changed_list = ['href="https://www.fabico.vn/"', 'f35a01', '<th style="text-align: left;">']

    # Khai báo biến chuỗi tạm thời & số chuỗi cần thêm
    temp_string = ''
    numFind_change = len(change_list)
    
    # Thay đổi các ký tự trong change_list thành changed_list
    for numfind in range(0, numFind_change):
        temp_string = str(html_string)
        html_string = ''
        html_string = repalce_str_html(temp_string, change_list[numfind], changed_list[numfind])

    return html_string
# Kết quả hàm thêm chuỗi

# Hàm chỉnh sửa mô tả theo định dạng người dùng
def format_description(html_string, name_product):
    '''
    Function: Định dạng lại các thẻ trong html như mong muốn
    - html_string: chuỗi cần xử lý và trả về chuỗi đã định dạng
    - name_product: tên sản phẩm
    Return về chuỗi có dịnh dạng ngon lành
    '''

    # Gọi các hàm thêm xóa mô tả
    html_string = delete_str_unnecessary(html_string)
    html_string = add_str_description(html_string)

    # Xóa chuỗi tên sản phẩm
    strResult = str(html_string)
    strResult.replace(name_product, "")

    # Tách thành các chuỗi con
    list_description = split_big_str(strResult, "</table>", 1, 0)

    # Định dạng heading cho tên sản phẩm
    name_h2 = "<h2>" + name_product + "</h2>\n"
    name_h3 = "<h3>" + name_product + "</h3>\n"

    # Thêm định dạng các thẻ theo định dạng
    description_1 = name_h2 + "<div>" + list_description[0] + "</table>" + "</div>"
    description_2 = "<hr/>" + name_h3 + list_description[1]

    return description_1 + description_2
# Kết thúc hàm chỉnh sửa mô tả theo định dạng người dùng