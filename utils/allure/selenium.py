from utils.allure.html import allure_html_img_base64_string
from utils.selenium.screenshot import png_base64_string_full_page


def allure_html_img_full_page(wd):
    base64_string = png_base64_string_full_page(wd)
    allure_html_img_base64_string(base64_string)
