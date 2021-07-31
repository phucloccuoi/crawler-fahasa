import handing_string

# Hàm đọc tất cả các dòng trong file vào danh sách
def list_info_input_product():
    '''
    - Chức năng: đưa tất cả các dòng trong file vào danh sách
    - list_all_lines_of_file: hàm trả về danh sách các dòng của file thông tin
    '''
    # Mở file dưới chứa thông tin sản phẩm và đọc chúng
    fileInput = open("input.txt", 'r+', encoding='utf-8')

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
    - result: số thứ tự chuỗi con trong một hàng
    '''
    result = handing_string.split_big_string(list_info_input_product()[ordinal_number_product])[number_sub_str]
    return result
# Kêt thúc hàm lấy ra thông tin từ file input.txt