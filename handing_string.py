from re import compile, sub

# Hàm chia nhỏ chuỗi lớn thành các chuỗi con
def split_big_string(input_string):
    '''
    - Chức năng: chia nhỏ chuỗi lớn thành các chuỗi con và cho vào dánh sách
    - input_string: chuỗi đầu vào cần được chia nhỏ
    - list_sub_string: hàm trả về danh sách chuỗi con
    '''
    # Tách các chuỗi thành chuỗi con khi gặp dấu phẩy, và tối đa là 4 chuỗi con
    list_sub_string = input_string.split(",", 4)

    # Xóa ký tự xuống dòng trong string
    temp = list_sub_string[4]
    temp = temp.rstrip("\n")
    list_sub_string[4] = temp

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

# Hàm chỉnh sửa mô tả theo định dạng người dùng
def edit_format_description(html_string, name_product):
    '''
    - Chức năng: Định dạng lại các thẻ trong html như mong muốn
    - html_string: chuỗi cần xử lý và trả về chuỗi đã định dạng
    '''
    # Thêm thẻ h2 vào đầu hàng với dữ liệu là tên sản phẩm
    name_product = "<h2>" + name_product + "</h2>\n"

    # Danh sách các chuỗi sẽ xóa
    black_list = ['\sclass="[a-z _-]+"', '<(\/)?col.*?>', '<div></div>']

    # Danh sách cac chuỗi sẽ thay đổi
    change_list = ['href="+(.*)?"', 'F39801', '<th>']
    changed_list = ['href="https://www.fabico.vn/"', 'f35a01', '<th style="text-align: left;">']

    # Khai báo biến lưu trữ tạm thời chuỗi
    temp_string = ''

    # Xóa các ký tự không cần thiết trong black_list
    for numfind in range(0, 3):
        temp_string = html_string
        html_string = ''
        html_string = repalce_str_html(temp_string, black_list[numfind], '')
    
    # Thay đổi các ký tự trong change_list thành changed_list
    for numfind in range(0, 3):
        temp_string = html_string
        html_string = ''
        html_string = repalce_str_html(temp_string, change_list[numfind], changed_list[numfind])

    # Trả về biến đầu vào sau khi xử lý
    return (name_product + html_string)
# Kết thúc hàm chỉnh sửa mô tả theo định dạng người dùng