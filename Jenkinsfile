pipeline {

  environment {
    registry = "zcrnivec/sample-app"
    registryCredential = 'dockerhub'
    dockerImage = ''
  }

  agent any

  stages {

    stage('Cloning Git') {
      steps {
        git 'https://github.com/zcrnivec/demo-pipeline.git'
      }
    }

    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
        }
      }
    }

    stage('Push Image') {
      steps{
        script {
          docker.withRegistry( "", registryCredential) {
            dockerImage.push()
          }
        }
      }
    }

    stage('Deploy App') {
      steps {
        script {
          kubernetesDeploy(configs: "sample-app.yaml", kubeconfigId: "kubeconfig")
        }
      }
    }

    stage('Remove Unused docker image') {
      steps{
        sh "docker rmi $registry:$BUILD_NUMBER"
      }
    }

  }

}