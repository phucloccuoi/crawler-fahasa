import handing_string

with open('referances.html', 'r+', encoding='utf8') as file:
    hello = file.read()
    with open('form_html.html', 'w+', encoding='utf8') as file_out:
        hello = handing_string.get_description_SEO(hello, 'TEST')
        file_out.write(hello)
        file_out.close()
file.close()