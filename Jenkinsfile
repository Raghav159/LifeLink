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

        stage('Backend Unit Tests') {
            steps {
                echo "🧪 Running Backend Tests..."
                sh '''
                cd backend
                python -m pip install --quiet -r requirements.txt
                python -m pytest --cov=app --cov-report=xml --cov-report=html --junit-xml=test-results.xml
                '''
            }
        }

        stage('Frontend Unit Tests') {
            steps {
                echo "🧪 Running Frontend Tests..."
                sh '''
                cd frontend
                npm install --legacy-peer-deps --silent
                npm run test -- --run --reporter=verbose
                '''
            }
        }

        stage('Build Backend Image') {
            steps {
                echo "🐳 Building Backend Docker Image..."
                sh '''
                docker build -f Dockerfile.backend -t $BACKEND_IMAGE .
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                echo "🐳 Building Frontend Docker Image..."
                sh '''
                docker build -f Dockerfile.frontend -t $FRONTEND_IMAGE .
                '''
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
        always {
            echo "📊 Archiving Test Results..."
            // Archive backend test results
            junit testResults: 'backend/test-results.xml', allowEmptyResults: true
            
            // Archive backend coverage report
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'backend/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Backend Coverage Report'
            ])
        }
        success {
            echo "✅ CI/CD Pipeline Successful - All tests passed and containers running!"
        }
        failure {
            echo "❌ CI/CD Pipeline Failed - Check test results above"
        }
    }
}