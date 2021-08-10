import handing_string

# Hàm đọc tất cả các dòng trong file vào danh sách
def read_file_to_list(file_name):
    '''
    - Chức năng: đưa tất cả các dòng trong file vào danh sách
    - list_all_lines_of_file: hàm trả về danh sách các dòng của file thông tin
    '''
    # Mở file dưới chứa thông tin sản phẩm và đọc chúng
    fileInput = open(file_name, 'r+', encoding='utf-8')

    # Lưu tất cả các dòng của file vào danh sách
    list_all_lines_of_file = fileInput.readlines()

    # Đòng file thông tin sản phẩm
    fileInput.close()

    return list_all_lines_of_file
# Kết thúc hàm đọc tất cả các dòng trong file vào danh sách

# Hàm lấy ra thông tin từ file input.txt
def get_info_from_file(ordinal_number_product, number_sub_str):
    '''
    - Chức năng: lấy ra giá từ file thông tin sản phẩm
    - result: trả về 1 chuỗi con tương ứng với number_sub_str truyền vào
    - ordinal_number_product: số thứ tự của sản phẩm trong file thông tin sản phẩm
    '''
    result = handing_string.split_big_str(read_file_to_list('input.txt')[ordinal_number_product], ",", 4, 1)[number_sub_str]
    return result
# Kêt thúc hàm lấy ra thông tin từ file input.txt

# Hàm ghi các barcode không tìm thấy vào file
def write_list_to_file(list_input, len_list, file_name):
    '''
    - Function: Ghi danh sách vào file chỉ định
    - Return: 1 nếu không có lỗi gì
    '''
    with open(file_name, 'w+', encoding='utf-8') as file_log:
        for index in range(0, len_list):
            file_log.writelines(list_input[index])
    file_log.close()

    return 1
# Kết thúc hàm ghi các barcode không tìm thấy vào file