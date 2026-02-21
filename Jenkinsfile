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


        stage('Prepare Environment Variables') {
            steps {
                script {
                    if (params.ENV == 'fat') {
                        // 如果选了 fat，就把 fat 的值赋给通用变量
                        env.DEVELOPER_ID = env.DEVELOPER_ID_FAT
                        env.E_POI_ID = env.E_POI_ID_FAT
                        env.SIGN = env.SIGN_FAT
                        env.BASE_URL = env.BASE_URL_FAT
                    } else if (params.ENV == 'uat') {
                        // 如果选了 uat，就把 uat 的值赋给通用变量
                        env.DEVELOPER_ID = env.DEVELOPER_ID_UAT
                        env.E_POI_ID = env.E_POI_ID_UAT
                        env.SIGN = env.SIGN_UAT
                        env.BASE_URL = env.BASE_URL_UAT
                    }
                }
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
                :: 运行 pytest 并指定 allure 结果存放目录
                :: --alluredir 参数告诉 pytest 把原始数据丢到 allure-results 文件夹
                pytest -v --junitxml=report.xml --alluredir=allure-results || exit 0
                '''
            }
        }
    }

    post {
        always {
            // 这里的 'allure' 必须对应你在“全局工具配置”中设置的别名
            // results: [path: 'allure-results'] 对应上面 pytest 生成数据的目录
            script {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }

            // 原有的 junit 也可以保留
            junit 'report.xml'
        }
    }
}