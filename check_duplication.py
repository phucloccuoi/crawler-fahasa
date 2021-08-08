import access_website
import os

# Hàm đọc tất cả các dòng trong file vào danh sách
def list_info_input_product():
    '''
    - Function: Đưa tất cả các dòng trong file vào danh sách
    - Return: Danh sách các dòng của file thông tin
    '''
    # Mở file dưới chứa thông tin sản phẩm và đọc chúng
    fileInput = open("input.txt", 'r+', encoding='utf-8')

    # Lưu tất cả các dòng của file vào danh sách
    list_all_lines_of_file = fileInput.readlines()

    # Đòng file thông tin sản phẩm
    fileInput.close()

    return list_all_lines_of_file
# Kết thúc hàm đọc tất cả các dòng trong file vào danh sách

# Hàm ghi các barcode không tìm thấy vào file
def write_error_barcode(list_barcode, len_list):
    # Gọi hàm lấy đường dẫn tại vị trí hiên tại
    path_curent = os.getcwd()

    try: # Nếu file đã có thì xóa file
        os.remove(path_curent + '\error_products.log')
    except FileNotFoundError: # Nếu file không có thì tạo file
        with open((path_curent + '\error_products.log'), 'w', encoding='utf-8') as file_log:
            print('>>> File error_products.log has been created successfully')
        file_log.close()
    finally: # Đều ghi lại barcode vào file
        with open('error_products.log', 'w+', encoding='utf-8') as file_log:
            for index in range(0, len_list):
                file_log.writelines(list_barcode[index])
        file_log.close()
# Kết thúc hàm ghi các barcode không tìm thấy vào file

# Khai báo các biến cần thiết
list_barcode = list_info_input_product()
list_not_Found = []
count = 0

# Tìm kiếm từng sản phẩm xem có đăng chưa
for barcode in list_barcode:
    # Khai báo đường dẫn truy cập webiste
    url_full = f"https://www.fabico.vn/search?type=product&q={barcode}"

    # Truy cập vào trang tìm kiếm
    search_page = access_website.get_session(url_full, 4)

    # Tìm kiếm tới thẻ có chứa kết quả tìm kiếm
    find_link = search_page.find("span.collection-size", first=True)

    # Nếu không tìm thấy sẽ ghi barcode đó vào danh sách log
    if find_link.text == '(0 sản phẩm)':
        print(f"- Product {count} not found!")
        list_not_Found.append(barcode)
    else: # Ngược lại nếu tìm thấy thì thôi
        print(f"- Product {count} had found!")
    count += 1

# Gọi hàm ghi danh sách vào file
write_error_barcode(list_not_Found, len(list_not_Found))

print("-----FINISH--------")