import allure


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
