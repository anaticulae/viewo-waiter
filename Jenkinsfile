pipeline{
    agent{
        docker{
            image '169.254.149.20:6001/arch_python_baw:0.10.6'
            args  '-v $WORKSPACE:/var/workdir'
        }
    }

    parameters{
        string(name: 'BRANCH', defaultValue: 'master')
        booleanParam(name: 'RELEASE', defaultValue: false)
    }

    stages{
        stage('sync'){
            steps{
                sh 'baw sync all'
                sh 'baw sh "pip install ."'
            }
        }
        stage('all'){
            steps{
                sh 'baw test all -n4 --cov --junit_xml=report.xml'
                junit '**/report.xml'
            }
        }
        stage('lint'){
            steps{
                sh 'baw lint'
            }
        }
        stage('release'){
            when {
                expression { return params.RELEASE }
            }
            steps{
                sh 'baw install && baw release && baw publish'
                // TODO: GIT COMMIT?
            }
        }
    }
}
