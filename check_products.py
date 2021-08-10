import access_website

# Hàm đọc tất cả các dòng trong file vào danh sách
def list_info_input_product(file_name):
    '''
    - Function: Đưa tất cả các dòng trong file vào danh sách
    - Return: Danh sách các dòng của file thông tin
    '''
    # Mở file dưới chứa thông tin sản phẩm và đọc chúng
    fileInput = open(file_name, 'r+', encoding='utf-8')

    # Lưu tất cả các dòng của file vào danh sách
    list_all_lines_of_file = fileInput.readlines()

    # Đòng file thông tin sản phẩm
    fileInput.close()

    return list_all_lines_of_file
# Kết thúc hàm đọc tất cả các dòng trong file vào danh sách

# Hàm ghi các barcode không tìm thấy vào file
def write_error_barcode(list_barcode, len_list, file_name):
    with open(file_name, 'w+', encoding='utf-8') as file_log:
        for index in range(0, len_list):
            file_log.writelines(list_barcode[index])
    file_log.close()
# Kết thúc hàm ghi các barcode không tìm thấy vào file

# Hàm kiểm tra sản phẩm có trên website hay không
def check_products_has_not(list_barcode, url_destination, research_tag, return_str, markup_str):
    list_return = []
    count = 0

    # Tìm kiếm từng sản phẩm xem có đăng chưa
    for barcode in list_barcode:
        # Truy cập vào trang tìm kiếm
        search_page = access_website.get_session(url_destination + barcode, 4)

        # Tìm kiếm tới thẻ có chứa kết quả tìm kiếm
        find_link = search_page.find(research_tag, first=True)
        
        if markup_str == 'fahasa': # Nếu đang kiểm tra trên fahasa
            if find_link == None: # Nếu find_link bằng None tức là có sản phẩm trên fahasa
                print(f"\_Product {count} on {markup_str}")
                list_return.append(barcode)
            else: # Ngược lại là không có sản phẩm
                print(f"\_Product {count} not found!")
        else:  # Ngược lại là đang kiểm tra trên fabico
            if find_link.text == return_str: # Nếu không tìm thấy sẽ ghi barcode đó vào danh sách log
                print(f"\_Product {count} not available on {markup_str}")
                list_return.append(barcode)
            else: # Ngược lại không tìm thấy sản phẩm
                print(f"\_Product {count} had found!")
        count += 1

    return list_return
# Kết thúc hàm kiểm tra sản phẩm trên website

# Khai báo các tên file
name_file_input = 'input_check.txt'
name_file_fabico = 'fabico.log'
name_file_fahasa = 'fahasa.log'

# Khai báo đường dẫn truy cập webiste
url_fabico = "https://www.fabico.vn/search?type=product&q="
url_fahasa = "https://www.fahasa.com/catalogsearch/result/?q="

# Khai báo danh sách barcode đầu vào
list_barcode_first_filter = list_info_input_product(name_file_input)
print('--CHECK IN STARTS FABICO--')

# Gọi hàm xử kiểm tra sản phẩm fabico và ghi vào file
list_not_Found_Fabico = check_products_has_not(list_barcode_first_filter, url_fabico, 'span.collection-size', '(0 sản phẩm)', 'fabico') # FABICO
write_error_barcode(list_not_Found_Fabico, len(list_not_Found_Fabico), name_file_fabico)

# Khai báo danh sách barcode không có trên fabico
list_barcode_second_filter = list_info_input_product(name_file_fabico)
print('--CHECK IN STARTS FAHASA--')

# Gọi hàm xử kiểm tra sản phẩm fahasa và ghi vào file
list_product_on_Fahasa = check_products_has_not(list_barcode_second_filter, url_fahasa, 'p.note-msg', 'Không có sản phẩm phù hợp với từ khóa tìm kiếm của bạn.', 'fahasa') # FAHASA
write_error_barcode(list_not_Found_Fabico, len(list_product_on_Fahasa), name_file_fahasa)

print("-------FINISH--------")