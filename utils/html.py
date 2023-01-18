import allure

from utils.selenium.screenshot import png_base64_string_full_page


def allure_html_img_base64_string(base64_string, alt=None):
    allure.dynamic.description_html(f"""<img src="data:image/png;base64, {base64_string}" alt="{alt if alt else 'img'}"/>""")


def allure_html_list(array):
    allure.dynamic.description_html(f"""<ul>{''.join(f"<li>{i}</li>" for i in array)}</ul>""")


def allure_html_table(df):
    html = df.style.set_table_styles([
        {"selector": "", "props": [("border", "1px solid grey")]},
        {"selector": "tbody td", "props": [("border", "1px solid grey")]},
    ])
    html = html.set_properties(**{'text-align': 'right'})
    html = html.to_html(index_names=False, index=False, encoding='utf-8')
    allure.dynamic.description_html(f"""
        <html lang="ru">
            <head>
              <meta charset="UTF-8">
            </head>
            <body>
                {html}
            </body>
        </html>
        """)


def allure_html_img_full_page(wd):
    base64_string = png_base64_string_full_page(wd)
    allure_html_img_base64_string(base64_string)
