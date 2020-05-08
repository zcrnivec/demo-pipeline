/*
	Copyright (c) 2020 Cisco and/or its affiliates.

	This software is licensed to you under the terms of the Cisco Sample
	Code License, Version 1.1 (the "License"). You may obtain a copy of the
	License at

		       https://developer.cisco.com/docs/licenses

	All use of the material herein must be in accordance with the terms of
	the License. All rights not expressly granted by the License are
	reserved. Unless required by applicable law or agreed to separately in
	writing, software distributed under the License is distributed on an "AS
	IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
	or implied.
*/

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
          sh "pip3 install -r requirements.txt"
          sh "python3 send_message.py '${env.BRANCH_NAME}' '${currentBuild.fullDisplayName}' '${BUILD_URL}/logText/progressiveText?start=0' 'SUCCESSFUL' '${BUILD_NUMBER}'"
      }
      failure {
          echo 'Failed'
          sh "pwd"
          sh "pip3 install -r requirements.txt"
          sh "python3 send_message.py '${env.BRANCH_NAME}' '${currentBuild.fullDisplayName}' '${BUILD_URL}/logText/progressiveText?start=0' 'FAILED' '${BUILD_NUMBER}'"
      }
  }
}