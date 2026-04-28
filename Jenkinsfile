pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "lifelink-backend:v1"
        FRONTEND_IMAGE = "lifelink-frontend:v1"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "📥 Cloning Repository..."
                git 'https://github.com/Raghav159/LifeLink'
            }
        }

        stage('Build Backend Image') {
            steps {
                echo "🐳 Building Backend Docker Image..."
                sh 'docker build -f Dockerfile.backend -t $BACKEND_IMAGE .'
            }
        }

        stage('Build Frontend Image') {
            steps {
                echo "🐳 Building Frontend Docker Image..."
                sh 'docker build -f Dockerfile.frontend -t $FRONTEND_IMAGE .'
            }
        }

        stage('Run Containers') {
            steps {
                echo "🚀 Starting Containers..."
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
