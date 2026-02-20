pipeline {
    agent any

    environment {
        DEFAULT_TIMEOUT = "10"
        WECHAT_WEBHOOK = ""
    }

    parameters {
        choice(name: 'ENV', choices: ['fat', 'uat'], description: '选择运行环境')
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
                D://python/python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat "pytest -v --env=${params.ENV} --junitxml=report.xml"
            }
        }
    }

    post {
        always {
            junit 'report.xml'
        }
    }
}