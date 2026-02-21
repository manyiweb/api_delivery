pipeline {
    agent any

    parameters {
        choice(
            name: 'ENV',
            choices: ['fat', 'uat'],
            description: '选择运行环境'
        )
    }

    environment {
        // 当前环境
        ENV = "${params.ENV}"

        // =========================
        // FAT 环境变量
        // =========================
        BASE_URL_FAT = "http://fat-pos.reabam.com:60030/api"

        DEVELOPER_ID_FAT = "106825"
        E_POI_ID_FAT = "reabamts_5ad586a8721e49518998aedef9fd3b5c"
        SIGN_FAT = "146bcdd348c4f7e90895af13faa123e201fe2686"

        // =========================
        // UAT 环境变量
        // =========================
        BASE_URL_UAT = "https://pos.reabam.com/api"

        DEVELOPER_ID_UAT = "106824"
        E_POI_ID_UAT = "reabam_b0213de5ff174215b056dcf40193ee78"
        SIGN_UAT = "146bcdd348c4f7e90895af13faa123e201fe2686"

        // =========================
        // 通用配置
        // =========================
        DEFAULT_TIMEOUT = "10"
        RETRY_TIMES = "3"
        RETRY_INTERVAL = "2"

        LOG_LEVEL = "INFO"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                set PYTHONUTF8=1
                D:\\python\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
                set PYTHONUTF8=1

                set ENV=fat
                set BASE_URL=http://fat-pos.reabam.com:60030/api
                set UAT_URL=https://pos.reabam.com/api

                echo BASE_URL=%BASE_URL%

                D:\\python\\python.exe -m pip install -r requirements.txt
                pytest -v --junitxml=report.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'report.xml'
        }
    }
}