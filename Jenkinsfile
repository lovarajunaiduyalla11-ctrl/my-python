pipeline {
  agent any

  parameters {
    string(name: 'DOCKERHUB_REPO', defaultValue: 'yourdockerhubuser/myapp', description: 'Docker Hub repo (user/repo)')
    string(name: 'REMOTE_HOST', defaultValue: 'your.remote.host', description: 'IP or hostname of remote server')
    string(name: 'REMOTE_USER', defaultValue: 'ubuntu', description: 'SSH user on remote')
    string(name: 'CONTAINER_NAME', defaultValue: 'myapp', description: 'Name for running container on remote')
    string(name: 'EXPOSE_PORT', defaultValue: '8080', description: 'Host port to bind on remote')
  }

  environment {
    IMAGE_TAG = "${env.BUILD_ID}"
    ARTIFACT_NAME = "app-${env.BUILD_ID}.zip"
    DOCKER_CREDENTIALS_ID = "docker-hub-creds"   // create in Jenkins (Username/Password)
    SSH_CREDENTIALS_ID = "ssh-remote"             // create in Jenkins (SSH private key)
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Run tests') {
      steps {
        // run tests inside ephemeral python container to avoid depending on Jenkins OS Python
        sh """
          docker run --rm -v "$PWD":/app -w /app python:3.10 bash -lc "pip install -r requirements.txt && pytest -q"
        """
      }
    }

    stage('Build artifact') {
      steps {
        sh "zip -r ${ARTIFACT_NAME} . -x .git\\*"
        archiveArtifacts artifacts: "${ARTIFACT_NAME}", fingerprint: true
      }
    }

    stage('Build Docker image') {
      steps {
        sh "docker build -t ${params.DOCKERHUB_REPO}:${IMAGE_TAG} ."
      }
    }

    stage('Docker login & push') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
          sh "docker push ${params.DOCKERHUB_REPO}:${IMAGE_TAG}"
          // optional: tag as latest
          sh "docker tag ${params.DOCKERHUB_REPO}:${IMAGE_TAG} ${params.DOCKERHUB_REPO}:latest || true"
          sh "docker push ${params.DOCKERHUB_REPO}:latest || true"
        }
      }
    }

    stage('Deploy to remote host') {
      steps {
        // requires SSH Agent plugin and an SSH credential configured in Jenkins
        sshagent (credentials: [env.SSH_CREDENTIALS_ID]) {
          sh """
            ssh -o StrictHostKeyChecking=no ${params.REMOTE_USER}@${params.REMOTE_HOST} \
            'docker pull ${params.DOCKERHUB_REPO}:${IMAGE_TAG} && \
             docker rm -f ${params.CONTAINER_NAME} || true && \
             docker run -d --name ${params.CONTAINER_NAME} -p ${params.EXPOSE_PORT}:8080 --restart=always ${params.DOCKERHUB_REPO}:${IMAGE_TAG}'
          """
        }
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
