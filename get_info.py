# Khai báo các modules cần sử dụng
from datetime import datetime
import csv
from requests_html import HTMLSession, HTML
import handing_string
from pyppeteer import errors

list_all_links_product = [] # Danh sách các link sản phẩm
list_all_html_products = [] # Danh sách các respone trả về

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
    - number_sub_str: số thứ tự chuỗi con trong một hàng
    '''
    result = handing_string.split_big_string(list_info_input_product()[ordinal_number_product])[number_sub_str]
    return result
# Kêt thúc hàm lấy ra thông tin từ file input.txt

# Hàm tạo một phiên kết nối vào một website với liên kêt cho trước
def get_session(url_full):
    '''
    - Chức năng: tạo một phiên kết nối vào một website với liên kêt cho trước
    - url_full: địa chỉ website muốn truy cập
    - result_page: hàm trả về biến loại HTML lưu toàn bộ thông tin html của website
    '''
    # Khởi tạo một phiên kết nối
    my_session = HTMLSession()

    # Tạo một phiên kết nối tới trang đích
    my_response = my_session.get(url_full)

    # Tổng thời gian Loading bằng thời gian tối đa là 6s + 2s và tối thiểu là 2s + 2s
    try:
        my_response.html.render(scrolldown=1, sleep=6, keep_page=True)
    except ConnectionRefusedError:
        my_response.html.render(scrolldown=1, sleep=7, keep_page=True)
    except RuntimeError:
        my_response.html.render(scrolldown=1, sleep=8, keep_page=True)
    except errors.NetworkError:
         my_response.html.render(scrolldown=1, sleep=5, keep_page=True)
    finally:
        my_session.close()

    # Lưu kết quả trả về với định dạng theo kiểu HTML
    result_page = HTML(html = my_response.html.html)

    return result_page
# Kết thúc hàm tạo một phiên kết nối vào một website với liên kêt cho trước

# Hàm lấy link sản phẩm từ trang tìm kiếm
def get_link_product(barcode):
    '''
    - Chức năng: lấy ra chính xác link sản phẩm 
    - Hàm trả về 1: nếu thêm thành công link sản phẩm vào danh sách
    - Hàm trả về -1: nếu sản phẩm không có trên trang fahasa, vẫn lưu vào danh sách respone rỗng
    - ordinal_number_product: số thứ tự của sản phẩm trong file thông tin
    '''
    # Truy cập tới trang tìm kiếm sản phẩm
    search_page = get_session(f"https://www.fahasa.com/search?in_stock=0&q={barcode}")

    try:
        # Tìm kiếm tới thẻ có chứa link sản phẩm
        find_link = search_page.find("div.item-inner", first=True)
        link_product = find_link.find("a.product-image", first=True)
    except AttributeError:
        # Nếu không tìm thấy sản phẩm thì lưu vào danh sách chuỗi rỗng
        list_all_links_product.append('')
        list_all_html_products.append('')
        return -1

    # Thêm chuỗi chứa link sản phẩm vào dánh sách
    list_all_links_product.append(str(link_product.attrs["href"]))

    return 1
# Kết thúc hàm lấy link sản phẩm từ trang tìm kiếm

# Hàm truy cập vào trang sản phẩm
def access_product_page(ordinal_number_product):
    '''
    - Chức năng: Truy cập vào trang sản phẩm 
    - ordinal_number_product: số thứ tự của sản phẩm trong file thông tin
    - product_page: Hàm trả về giá trị có kiêu HTML của trang đích
    '''
    # Lấy url sản phẩm từ danh sách
    url_product = list_all_links_product[ordinal_number_product]
    
    # Truy cập tới trang sản phẩm
    product_page = get_session(url_product)

    # Thêm respone sản phẩm vào danh sách lưu trữ respone
    list_all_html_products.append(product_page)

    # Vẫn phải trả về kết quả do luồng truy cập đầu tiên từ hàm khác
    return product_page
# Kết thúc hàm truy cập vào trang sản phẩm

# Hàm lấy ra tên sản phẩm
def get_name_product(ordinal_number_product):
    '''
    - Chức năng: lấy ra tên sản phẩm
    - name_product: trả về tên sản phẩm cần tìm
    - ordinal_number_product: số thứ tự của sản phẩm trong file thông tin sản phẩm
    '''
    source_page = access_product_page(ordinal_number_product)

    # Tìm kiếm tên
    temp = source_page.find("a.include-in-gallery", first=True)
    name_product = temp.attrs["title"]

    return str(name_product)
# Kêt thúc hàm lấy ra tên sản phẩm

# Hàm lấy thông tin Url theo đinh dạng "viet-chi-staedtler-134-2b"
def get_link_to_format(ordinal_number_product):
    '''
    - Chức năng: Lấy chuỗi theo định dạng cuỗi link Ex:viet-chi-staedtler-134-2b
    - ordinal_number_product: số thứ tự của sản phẩm trong file thông tin
    - url_short: Hàm trả về giá trị có kiểu chuỗi có đinh dạng cho theo yêu cầu
    '''
    url_product = list_all_links_product[ordinal_number_product]

    # Chuyển sang chuỗi
    url_short = str(url_product)

    return str(url_short[23:-5])
# Kết thúc lấy thông tin Url theo đinh dạng "viet-chi-staedtler-134-2b"

# Hàm lấy Link hình của sản phẩm
def get_all_links_images_product(ordinal_number_product):
    '''
    - Chức năng: Lấy tất cả các link hình ảnh của sản phẩm và lưu vào danh sách
    - list_links_images: Trả về danh sách các link của sản phẩm
    - ordinal_number_product: số thứ tự của sản phẩm trong file thông tin
    '''
    # Truy cập vào trang sản phẩm
    source_page = list_all_html_products[ordinal_number_product]

    # Tìm kiếm các link hình trong trang sản phẩm
    find_element1 = source_page.find("div.swiper-wrapper", first=True)
    find_element2 = find_element1.find("img.swiper-lazy")
    
    # Tạo danh sách lưu các link
    list_links_images = []

    # Gán các link tìm được vào danh sách
    for number_links in range(0, len(find_element2)):
        list_links_images.append(find_element2[number_links].attrs["src"])
    
    # Trả về danh sách các link của sản phẩm
    return list_links_images
# Kết thúc hàm lấy Link hình của sản phẩm

# Hàm lấy mô tả của sản phẩm và định dạng theo chuẩn
def get_description(ordinal_number_product, name_product):
    '''
    - Chức năng: lấy các giá trị mô tả trong phần mô tả sản phẩm
    - string_description_product: trả về chuỗi thu về từ trang đích
    - ordinal_number_product: số thứ tự của sản phẩm trong file thông tin
    - name_product: lấy tên sản phẩm cho vào phần mô tả
    '''
    # Truy cập vào trang sản phẩm
    source_page = list_all_html_products[ordinal_number_product]

    # Tìm kiếm các mô tả
    description_product = source_page.find("div.std", first=True)
    description_product_table = source_page.find("div.product_view_tab_content_additional", first=True)

    # Chuyển các giá trị html sang kiểu string
    try:
        string_description_product1 = str(description_product.html)
    except AttributeError:
        return -1
    string_description_product2 = str(description_product_table.html)

    # Thêm thẻ h2 vào chuỗi
    string_description_product = string_description_product2 + string_description_product1

    return handing_string.edit_format_description(string_description_product, name_product)
# Kết thúc hàm lấy mô tả của sản phẩm và định dạng theo chuẩn

# Hàm lấy thời gian hiện tại
def get_time_now():
    '''
    - Chức năng: lấy thời gian tại thời điểm hiện tại theo định dạng
    - formatTime: trả về chuỗi time theo định dạng Ngày/Tháng/Năm Giờ:Phút:Giây
    '''
    # Lấy thời gian hiện tại
    timeNow = datetime.now()

    # Định dạng thời gian
    formatTime = timeNow.strftime("%d/%m/%Y %H:%M:%S")

    return formatTime
# Kêt thúc hàm lấy thời gian hiện tại

# Hàm ghi các tiêu đề vào file output.csv
def write_header_to_file():
    '''
    - Chức năng: ghi tiêu đề vào file
    - Trả về 1: nếu việc ghi hoàn tất
    '''
    # Khai báo danh sách chuỗi các tiêu đề
    header = []
    with open('output.csv', 'w', newline = '', encoding='utf-8') as file_output:
            # Khai báo danh sách các tiêu đề
            headers = ['Url', 'Tên', 'Mô tả', 'Trích dẫn', 'Hãng', 'Loại sản phẩm', 'Tag', 'Hiển thị', 
                        'Thuộc tính 1', 'Giá trị thuộc tính 1', 'Thuộc tính 2', 'Giá trị thuộc tính 2', 
                        'Thuộc tính 3', 'Giá trị thuộc tính 3', 'Mã phiên bản sản phẩm', 'Khối lượng', 
                        'Quản lý tồn kho', 'Số lượng tồn kho', 'Đặt hàng khi hết hàng', 'Variant Fulfillment Service', 
                        'Giá', 'Giá so sánh', 'Có giao hàng không?', 'Variant Taxable', 'Barcode', 'Link hình', 
                        'Mô tả hình', 'Gift Card', 'SEO Title', 'SEO Description', 'Google Shopping / Google Product Category', 
                        'Google Shopping / Gender', 'Google Shopping / Age Group', 'Google Shopping / MPN', 
                        'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels', 'Google Shopping / Condition', 
                        'Google Shopping / Custom Product', 'Danh mục', 'Danh mục EN', 'Ảnh biến thể', 'Ngày tạo', 'Ngày cập nhật', 
                        'Hiển thị kênh bán hàng Lazada', 'Hiển thị kênh bán hàng Zalo', 'Hiển thị kênh bán hàng Zalora', 
                        'Hiển thị kênh bán hàng Sendo', 'Hiển thị kênh bán hàng Adayroi', 'Hiển thị kênh bán hàng FacebookShop', 
                        'Hiển thị kênh bán hàng Tiki', 'Hiển thị kênh bán hàng Google', 'Hiển thị kênh bán hàng Shopee', 
                        'Không áp dụng khuyến mãi', 'Hiển thị kênh bán hàng HaraRetail']
            
            # ghi các tiêu đề vào file
            writer = csv.writer(file_output, delimiter=',')
            writer.writerow(headers)

    file_output.close()
    return 1
# Kêt thúc hàm ghi các tiêu đề vào file output.csv

# Hàm ghi các giá trị thu thập được vào file
def write_info_to_file(ordinal_number_product):
    '''
    - Chức năng: ghi thông tin thu thập được vào file
    - Trả về 1: nếu việc ghi hoàn tất
    - Trả về -1: nếu không có sản phẩm trên fahasa, và lưu barcode lỗi vào error_products.log
    '''
    #----------------------------Khu vực kiểm tra các biến gán đầu vào-----------------------##
    # Giá trị cho cột Barcode
    barcode = get_info_from_file(ordinal_number_product, 0)
    result_page_product = get_link_product(barcode)

    if result_page_product == -1:
        print('>>> No products found!')

        # Nếu sản phẩm không có trên website hoặc lỗi thì lưu vào file
        with open('error_products.log', 'a+', encoding='utf-8') as error:
            error.writelines(barcode + '\n')
        error.close()
        return -1
    else:
    # Giá trị cột Url
        urlShort = get_link_to_format(ordinal_number_product)

        # Giá trị cho cột Tên sản phẩm
        nameProduct = get_name_product(ordinal_number_product)

        # Giá trị cho cột Mô tả
        decriptionProduct = get_description(ordinal_number_product, nameProduct)

        # Giá trị cho cột Nhà cung cấp
        valueProducer = get_info_from_file(ordinal_number_product, 3)

        # Giá trị cho cột loại sản phẩm
        type_product = get_info_from_file(ordinal_number_product, 2)

        # Giá trị cho cột Link hình
        list_link_images = get_all_links_images_product(ordinal_number_product)

        # Giá trị cho cột Ngày hiện tại và cột ngày cập nhập
        timeNow = get_time_now()

        # Khai báo số lượng sản phẩm và số hàng của từng sản phẩm
        number_imgages = len(get_all_links_images_product(ordinal_number_product))

        # Giá trị cột giá của sản phẩm
        price_product = get_info_from_file(ordinal_number_product, 1)
    #------------------------Kết thúc khu vực kiểm tra các biến gán đầu vào-----------------------##

        # Mở file output.csv và ghi các giá trị thu thập vào file
        with open('output.csv', 'a+', newline = '', encoding='utf-8') as file_output:
            
            # Khai báo đối tượng ghi file
            writer = csv.writer(file_output, delimiter=',')

            # Cho vòng lặp chạy tạo mỗi hình là một hàng
            for numberImages in range(0, number_imgages):
                value_row = [urlShort, nameProduct, decriptionProduct, 
                                    '', valueProducer, type_product, type_product, 'Yes', 
                                    'Title', 'Default Title', '', '', '', '', barcode, '0', 'Haravan', 
                                    '50', 'deny', '', price_product, price_product, 'Yes', 
                                    'Yes', barcode, list_link_images[numberImages], nameProduct, 
                                    'No', nameProduct, nameProduct, '', '', '', '', '', '', '', '', '', 
                                    '', '', timeNow, timeNow, 'No', 'No', 'No', 'No', 'No', 'No', 'No', 
                                    'Yes', 'No', 'No', 'Yes']
                value_row_image = [urlShort, '', '', '', '', '', '', 'Yes', '', '', '', '', '', '', 
                                    '', '', '', '0', 'deny', '', '', '', 'No', 'No', '', 
                                    list_link_images[numberImages], nameProduct, 'No', '', '', '', 
                                    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 
                                    '', '', '', '', 'No', 'No']
                if numberImages == 0:
                    writer.writerow(value_row)
                elif numberImages > 0:
                    writer.writerow(value_row_image)
        file_output.close()
        print(f"- Finish product {ordinal_number_product}")
    return 1
# Kết thúc hàm xóa ghi các giá trị thu thập được vào file