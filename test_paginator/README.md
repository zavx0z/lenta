# Сбор адресов страниц из пагинации

## Запуск теста

```shell
pytest test_paginator/test.py \
--url=https://lenta.com/catalog/bakaleya/ \
--schema=schema.xml \
--result=store/delivery/Бакалея.parquet
```

## Аргументы командной строки

--url

--schema

--parquet

## Запуск отчета

```shell
allure serve tmp/allure_results/
```