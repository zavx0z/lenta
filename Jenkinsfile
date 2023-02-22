pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '4', artifactNumToKeepStr: '4'))
        disableConcurrentBuilds(abortPrevious: true)
    }
    parameters {
        string( name: 'url', defaultValue: "https://lenta.com/catalog/bakaleya/", description: 'Адрес страницы')
        string( name: 'schema', defaultValue: "schema.xml", description: 'XML-схема страницы')
        string( name: 'result', defaultValue: "store/delivery/Бакалея.parquet", description: 'Parquet файл результатов')
        string( name: 'report', defaultValue: "tmp/allure_results", description: 'Директория отчетов')
    }
    environment {
        PYTEST_DEBUG=1
        STORE_DIR=./store
        CHROME_HOST='192.168.88.44'
        CHROME_PORT=4444
    }
    stages {
        stage('Установка зависимостей'){
            steps {
                withPythonEnv('python') {
                    sh 'python --version'
                    sh 'pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Тест пагинации') {
            steps {
                withPythonEnv('python') {
                    sh "pytest test_paginator/test_paginator.py --url=${params.url} --schema=${params.schema} --result=${params.result} --alluredir=${params.report}"
                }
            }
        }
    }
    post {
        always {
            script {
                allure includeProperties: false, jdk: '', results: [[path: params.report]]
            }
        }
    }
}