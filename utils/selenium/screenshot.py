def png_base64_bytes_element_full(element):
    driver = element.parent
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    base64_bytes = element.screenshot_as_png
    driver.maximize_window()
    return base64_bytes
