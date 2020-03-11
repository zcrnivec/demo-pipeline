pipeline {
  environment {
    registry = 'zcrnivec/sample-app'
    registryCredential = 'dockerhub'
    dockerImage = ''
    WEBEX_TEAMS_ACCESS_TOKEN = credentials('WEBEX_TEAMS_ACCESS_TOKEN')
    WEBEX_TEAMS_ROOM_ID = credentials('WEBEX_TEAMS_ROOM_ID')
    JENKINS_TOKEN = credentials('JENKINS_TOKEN')
  }

  agent any

  stages {
    stage('Cloning Git') {
      steps {
        git(url: 'https://github.com/zcrnivec/demo-pipeline.git', credentialsId: 'github')
      }
    }

    stage('Build image') {
      steps {
        script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
        }

      }
    }

    stage('Push Image') {
      steps {
        script {
          docker.withRegistry( "", registryCredential) {
            dockerImage.push()
          }
        }

      }
    }

    stage('Deploy App') {
      steps {
        sh "sed -i 's/BUILD_NUMBER/$BUILD_NUMBER/' sample-app.yaml"

        script {
          kubernetesDeploy(configs: "sample-app.yaml", kubeconfigId: "kubeconfig")
        }

      }
    }

    stage('Remove Unused docker image') {
      steps {
        sh "docker rmi $registry:$BUILD_NUMBER"
      }
    }

  }

  post {
      always {
        echo "${currentBuild.fullDisplayName}"
        echo "${currentBuild.result}"
        echo "reporting...}"
      }

      success {
          echo 'Success'
          sh "python3 send_message.py '${env.BRANCH_NAME}' '${currentBuild.fullDisplayName}' '${BUILD_URL}/logText/progressiveText?start=0' 'SUCCESSFUL' '${BUILD_NUMBER}'"
      }
      failure {
          echo 'Failed'
          sh "python3 send_message.py '${env.BRANCH_NAME}' '${currentBuild.fullDisplayName}' '${BUILD_URL}/logText/progressiveText?start=0' 'FAILED' '${BUILD_NUMBER}'"
      }
  }
}