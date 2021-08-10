import access_website
import handing_file

# Hàm kiểm tra sản phẩm có trên website hay không
def check_products_has_not(list_barcode, url_destination, research_tag, return_str, markup_str):
    '''
    Function: Kiểm tra sản phẩm có trên webiste đích không và lưu vào danh sách
    - list_barcode: Danh sách đầu vào cần kiểm tra
    - url_destination: Địa chỉ tìm kiếm sản phẩm của website
    - research_tag: Thẻ tìm kiếm kết quả trả về
    - return_str: Chuỗi thông báo kết quả tìm kiếm
    - markup_str: Phân biệt các trang website với nhau
    Return: Danh sách barcode
    '''
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
list_barcode_first_filter = handing_file.read_file_to_list(name_file_input)
print('--CHECK IN STARTS FABICO--')

# Gọi hàm kiểm tra sản phẩm fabico và ghi vào file
list_not_Found_Fabico = check_products_has_not(list_barcode_first_filter, url_fabico, 'span.collection-size', '(0 sản phẩm)', 'fabico') # FABICO
handing_file.write_list_to_file(list_not_Found_Fabico, len(list_not_Found_Fabico), name_file_fabico)

# Khai báo danh sách barcode không có trên fabico
list_barcode_second_filter = handing_file.read_file_to_list(name_file_fabico)
print('--CHECK IN STARTS FAHASA--')

# Gọi hàm kiểm tra sản phẩm fahasa và ghi vào file
list_product_on_Fahasa = check_products_has_not(list_barcode_second_filter, url_fahasa, 'p.note-msg', 'Không có sản phẩm phù hợp với từ khóa tìm kiếm của bạn.', 'fahasa') # FAHASA
handing_file.write_list_to_file(list_product_on_Fahasa, len(list_product_on_Fahasa), name_file_fahasa)

print("-------FINISH--------")