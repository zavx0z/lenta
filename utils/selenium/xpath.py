def sibling_text_content(wd, xpath):
    xpath_string = f"{xpath}/following-sibling::text()[1]"
    return wd.execute_script(f'return document.evaluate("{xpath_string}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.textContent;')
