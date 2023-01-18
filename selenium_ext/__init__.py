from time import sleep


def get_attributes(element):
    driver = getattr(element, "_parent")
    return driver.execute_script("""
    let items = {}
    for (let index = 0; index < arguments[0].attributes.length; ++index) {
        items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value
    }
    return items
    """, element)


def scroll_to_center(element):
    driver = getattr(element, "_parent")
    driver.execute_script("var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);var elementTop = arguments[0].getBoundingClientRect().top;window.scrollBy(0, elementTop-(viewPortHeight/2));", element)


def highlight(element, time=1.0):
    driver = getattr(element, "_parent")
    original_style = element.get_attribute('style')
    style = "border-color: red;"
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)
    sleep(time)
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)
