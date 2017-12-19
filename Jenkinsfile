pipeline {
  agent none
  options {
    ansiColor('xterm')
    timestamps()
  }
  stages {
    stage('Build') {
      parallel {
        // *************************** gcc49 ************************************
        stage('gcc49') {
          agent {
            docker {
              image 'ogs6/conangcc49'
              label 'docker'
              args '-v /home/jenkins/.ccache:/usr/src/.ccache'
              alwaysPull true
            }
          }
          environment {
            CONAN_REFERENCE = "Qt/5.9.2"
            JFROG = credentials('3a3e2a63-4509-43c9-a2e9-ea0c50fdcd4c')
            CONAN_USERNAME = "bilke"
            CONAN_CHANNEL = "testing"
            CONAN_UPLOAD = "https://ogs.jfrog.io/ogs/api/conan/conan"
            CONAN_STABLE_BRANCH_PATTERN = "release/*"
            CONAN_GCC_VERSIONS = "4.9"
            CONAN_USER_HOME = "$WORKSPACE/conan"
          }
          steps {
            script {
              withEnv(['CONAN_LOGIN_USERNAME=$JFROG_USR', 'CONAN_PASSWORD=$JFROG_PSW']) {
                sh 'sudo ./.travis/install.sh'
                sh 'conan user'
                sh './.travis/run.sh'
                sh 'rm -r $CONAN_USER_HOME'
              }
            }
          }
        }
        // *************************** gcc5 ************************************
        stage('gcc5') {
          agent {
            docker {
              image 'ogs6/conangcc5'
              label 'docker'
              args '-v /home/jenkins/.ccache:/usr/src/.ccache'
              alwaysPull true
            }
          }
          environment {
            CONAN_REFERENCE = "Qt/5.9.2"
            JFROG = credentials('3a3e2a63-4509-43c9-a2e9-ea0c50fdcd4c')
            CONAN_USERNAME = "bilke"
            CONAN_CHANNEL = "testing"
            CONAN_UPLOAD = "https://ogs.jfrog.io/ogs/api/conan/conan"
            CONAN_STABLE_BRANCH_PATTERN = "release/*"
            CONAN_GCC_VERSIONS = "5"
            CONAN_USER_HOME = "$WORKSPACE/conan"
          }
          steps {
            script {
              withEnv(['CONAN_LOGIN_USERNAME=$JFROG_USR', 'CONAN_PASSWORD=$JFROG_PSW']) {
                sh 'sudo ./.travis/install.sh'
                sh 'conan user'
                sh './.travis/run.sh'
                sh 'rm -r $CONAN_USER_HOME'
              }
            }
          }
        }
        // *************************** gcc6 ************************************
        stage('gcc6') {
          agent {
            docker {
              image 'ogs6/conangcc6'
              label 'docker'
              args '-v /home/jenkins/.ccache:/usr/src/.ccache'
              alwaysPull true
            }
          }
          environment {
            CONAN_REFERENCE = "Qt/5.9.2"
            JFROG = credentials('3a3e2a63-4509-43c9-a2e9-ea0c50fdcd4c')
            CONAN_USERNAME = "bilke"
            CONAN_CHANNEL = "testing"
            CONAN_UPLOAD = "https://ogs.jfrog.io/ogs/api/conan/conan"
            CONAN_STABLE_BRANCH_PATTERN = "release/*"
            CONAN_GCC_VERSIONS = "6"
            CONAN_USER_HOME = "$WORKSPACE/conan"
          }
          steps {
            script {
              withEnv(['CONAN_LOGIN_USERNAME=$JFROG_USR', 'CONAN_PASSWORD=$JFROG_PSW']) {
                sh 'sudo ./.travis/install.sh'
                sh 'conan user'
                sh './.travis/run.sh'
                sh 'rm -r $CONAN_USER_HOME'
              }
            }
          }
        }
        // *************************** gcc7 ************************************
        stage('gcc7') {
          agent {
            docker {
              image 'ogs6/conangcc7'
              label 'docker'
              args '-v /home/jenkins/.ccache:/usr/src/.ccache'
              alwaysPull true
            }
          }
          environment {
            CONAN_REFERENCE = "Qt/5.9.2"
            JFROG = credentials('3a3e2a63-4509-43c9-a2e9-ea0c50fdcd4c')
            CONAN_USERNAME = "bilke"
            CONAN_CHANNEL = "testing"
            CONAN_UPLOAD = "https://ogs.jfrog.io/ogs/api/conan/conan"
            CONAN_STABLE_BRANCH_PATTERN = "release/*"
            CONAN_GCC_VERSIONS = "7"
            CONAN_USER_HOME = "$WORKSPACE/conan"
          }
          steps {
            script {
              withEnv(['CONAN_LOGIN_USERNAME=$JFROG_USR', 'CONAN_PASSWORD=$JFROG_PSW']) {
                sh 'sudo ./.travis/install.sh'
                sh 'conan user'
                sh './.travis/run.sh'
                sh 'rm -r $CONAN_USER_HOME'
              }
            }
          }
        }
        // ************************** vs2017 ***********************************
        stage('vs2017') {
          agent {label 'win && conan' }
          environment {
            CONAN_REFERENCE = "Qt/5.9.2"
            JFROG = credentials('3a3e2a63-4509-43c9-a2e9-ea0c50fdcd4c')
            CONAN_USERNAME = "bilke"
            CONAN_CHANNEL = "testing"
            CONAN_UPLOAD = "https://ogs.jfrog.io/ogs/api/conan/conan"
            CONAN_STABLE_BRANCH_PATTERN = "release/*"
            CONAN_VISUAL_VERSIONS = "15"
            CONAN_USER_HOME = "$WORKSPACE\\conan"
          }
          steps {
            script {
              withEnv(['CONAN_LOGIN_USERNAME=%JFROG_USR%', 'CONAN_PASSWORD=%JFROG_PSW%']) {
                bat 'python build.py'
                bat 'rd /S /Q %CONAN_USER_HOME%'
              }
            }
          }
        }
      } // end parallel
    }
  }
}
