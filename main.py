# Khai báo các modules
import get_info
import handing_file
import os

# Khởi tạo biến tính số lượng sản phẩm trong file đầu vào
number_product = len(handing_file.read_file_to_list('input.txt'))

# Khởi tạo biến kiểm tra ghi tiếp hay không ghi tiếp là KHÔNG GHI
user_innput = 'n'

# Mời người dùng chọn có muốn ghi tiếp vào file hay không, mặc định là KHÔNG GHI
user_innput = input('Do you want to continue importing into the old file? (y/N)')

# Nếu muốn ghi tiếp thì OK men và không ghi tiêu đề
if user_innput == 'y':
    print('>>> OK men!!') 

# Nếu KHÔNG GHI tiếp thì xóa file và ghi tiếp và ghi tiêu đề trước tiên
elif user_innput == 'n':
    # Gọi hàm lấy đường dẫn tại vị trí hiên tại
    path_curent = os.getcwd()

    try: # Nếu file đã có thì xóa file
        os.remove(path_curent + '\output.csv')
        os.remove(path_curent + '\error_products.log')
    except FileNotFoundError: # Nếu file không có thì tạo file
        with open((path_curent + '\output.csv'), 'w', encoding='utf-8') as file_info:
            print('>>> File output.csv has been created successfully')
        file_info.close()
        with open((path_curent + '\error_products.log'), 'w', encoding='utf-8') as file_log:
            print('>>> File error_products.log has been created successfully')
        file_log.close()
    finally: # Đều ghi lại tiêu đề vào file
        get_info.write_header_to_file()

# Ghi các thông tin vào file
for main_loop in range(0, number_product):
    get_info.write_info_to_file(main_loop)
else:
    print('--------DONE!---------')