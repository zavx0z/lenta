import allure


def allure_html_img_base64_string(base64_string, alt=None):
    allure.dynamic.description_html(f"""<img src="data:image/png;base64, {base64_string}" alt="{alt if alt else 'img'}"/>""")


def allure_html_list(array):
    allure.dynamic.description_html(f"""<ul>{[f"<li>{i}</li>" for i in array]}</ul>""")
