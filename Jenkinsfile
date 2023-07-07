pipeline {
    environment {
        buildNumber = "${currentBuild.number}"
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
    }
  agent any
  stages {

    stage('Fetch Code From GitHub') {
      steps {
        git "https://github.com/tteog-ip/dash-back.git"
      }
    }

    stage('AWS Credentials') {
        steps {
            withAWS(credentials: 'AWS-KEY', region: 'ap-northeast-2') {
                sh 'aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 728156710202.dkr.ecr.ap-northeast-2.amazonaws.com/dash-back'
            }
        }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker system prune -f && docker build --force-rm --no-cache --tag 728156710202.dkr.ecr.ap-northeast-2.amazonaws.com/dash-back:v$buildNumber .'
      }
    }

    stage('ECR Push') {
        steps {
            sh 'docker push 728156710202.dkr.ecr.ap-northeast-2.amazonaws.com/dash-back:v$buildNumber'
        }
    }

    stage('Change Tag in GitHub') {
        steps{
                git branch: 'master', url: 'https://github.com/tteog-ip/app-argocd'
                dir('front') {
                  sh 'sed -i "s/image:.*$/image: 728156710202.dkr.ecr.ap-northeast-2.amazonaws.com\\/app-front:v$BuildNumber/g" deployment.yaml'
                  sh 'git add -u'
                  sh 'git commit -m "Update Image Tag - v$BuildNumber"'
                  withCredentials([gitUsernamePassword(credentialsId: 'github-token-cykim', gitToolName: 'Default')]) {
                      sh 'git push origin master'
                }
            }
        }
    }
  }
}
