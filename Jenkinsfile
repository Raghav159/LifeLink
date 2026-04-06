pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "lifelink-backend:v1"
        FRONTEND_IMAGE = "lifelink-frontend:v1"
    }

    stages {

        stage('Clone Code') {
            steps {
                git 'https://github.com/Raghav159/LifeLink.git'
            }
        }

        stage('Build Backend Image') {
            steps {
                sh '''
                docker build -f Dockerfile.backend -t $BACKEND_IMAGE .
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                docker build -f Dockerfile.frontend -t $FRONTEND_IMAGE .
                '''
            }
        }

        stage('Run Containers') {
            steps {
                sh '''
                docker rm -f backend || true
                docker rm -f frontend || true

                docker run -d -p 8000:8000 --name backend $BACKEND_IMAGE
                docker run -d -p 3000:80 --name frontend $FRONTEND_IMAGE
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD Pipeline Successful"
        }
        failure {
            echo "❌ CI/CD Pipeline Failed"
        }
    }
}