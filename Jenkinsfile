pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "lifelink-backend:v1"
        FRONTEND_IMAGE = "lifelink-frontend:v1"
    }

    stages {

        stage('Build Images in Minikube') {
            steps {
                echo "🐳 Building Images inside Minikube..."

                sh '''
                # Switch to Minikube Docker
                eval $(minikube docker-env)

                # Build images
                docker build -f Dockerfile.backend -t $BACKEND_IMAGE .
                docker build -f Dockerfile.frontend -t $FRONTEND_IMAGE .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "☸️ Deploying to Kubernetes..."

                sh '''
                kubectl apply -f k8s/

                kubectl rollout restart deployment backend || true
                kubectl rollout restart deployment frontend || true
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo "🔍 Checking pods..."

                sh '''
                kubectl get pods
                kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD Pipeline Successful (Auto Deployed to K8s)"
        }
        failure {
            echo "❌ CI/CD Pipeline Failed"
        }
    }
}
