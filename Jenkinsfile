pipeline {
    agent {
        label 'macos'
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
    }

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'smoke', 'regression', 'ntp', 'api'],
            description: 'Select test suite to run'
        )
        booleanParam(
            name: 'PARALLEL_EXECUTION',
            defaultValue: true,
            description: 'Enable parallel test execution'
        )
        string(
            name: 'NUM_WORKERS',
            defaultValue: '2',
            description: 'Number of parallel workers'
        )
    }

    environment {
        PYTHON_VERSION = '3.11'
        APPIUM_HOST = '127.0.0.1'
        APPIUM_PORT = '4723'
        VENV_PATH = "${WORKSPACE}/.venv"
        REPORTS_PATH = "${WORKSPACE}/reports"
        PATH = "${VENV_PATH}/bin:${PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    echo "🔄 Repository checked out successfully"
                    echo "Workspace: ${WORKSPACE}"
                }
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    echo "📦 Setting up Python environment"
                    sh '''
                        python3 --version
                        python3 -m venv ${VENV_PATH}
                        source ${VENV_PATH}/bin/activate
                        pip install --upgrade pip setuptools wheel
                        echo "✅ Virtual environment created"
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo "📥 Installing dependencies from requirements.txt"
                    sh '''
                        source ${VENV_PATH}/bin/activate
                        pip install -r requirements.txt
                        echo "✅ All dependencies installed"
                    '''
                }
            }
        }

        stage('Verify Xcode & Appium') {
            steps {
                script {
                    echo "🔍 Verifying Xcode and development tools"
                    sh '''
                        xcode-select --version
                        xcodebuild -version
                        
                        if ! command -v appium &> /dev/null; then
                            echo "Installing Appium..."
                            npm install -g appium
                        fi
                        
                        appium --version
                        echo "✅ Development tools verified"
                    '''
                }
            }
        }

        stage('Start Appium Server') {
            steps {
                script {
                    echo "🚀 Starting Appium server on ${APPIUM_HOST}:${APPIUM_PORT}"
                    sh '''
                        mkdir -p ${REPORTS_PATH}
                        pkill -f "appium" || true
                        sleep 2
                        
                        appium --port ${APPIUM_PORT} > ${REPORTS_PATH}/appium.log 2>&1 &
                        APPIUM_PID=$!
                        echo $APPIUM_PID > ${REPORTS_PATH}/appium.pid
                        
                        for i in {1..30}; do
                            if curl -s http://${APPIUM_HOST}:${APPIUM_PORT}/status > /dev/null 2>&1; then
                                echo "✅ Appium server is ready (PID: $APPIUM_PID)"
                                exit 0
                            fi
                            echo "⏳ Waiting for Appium server... ($i/30)"
                            sleep 2
                        done
                        
                        echo "❌ Failed to connect to Appium server"
                        exit 1
                    '''
                }
            }
        }

        stage('Prepare Test Environment') {
            steps {
                script {
                    echo "📋 Preparing test environment"
                    sh '''
                        mkdir -p ${REPORTS_PATH}/screenshots
                        mkdir -p ${REPORTS_PATH}/logs
                        rm -f ${REPORTS_PATH}/logs/test.log
                        echo "✅ Test environment prepared"
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "🧪 Running tests - Suite: ${params.TEST_SUITE}"
                    
                    def pytestCmd = "pytest"
                    def testPath = "tests/"
                    def markerOption = ""
                    
                    switch(params.TEST_SUITE) {
                        case 'smoke':
                            markerOption = "-m smoke"
                            break
                        case 'regression':
                            markerOption = "-m 'not skip'"
                            break
                        case 'ntp':
                            testPath = "tests/ntp/"
                            break
                        case 'api':
                            testPath = "tests/api/"
                            break
                        default:
                            markerOption = "-m 'not skip'"
                    }
                    
                    def parallelOption = ""
                    if (params.PARALLEL_EXECUTION) {
                        parallelOption = "-n ${params.NUM_WORKERS}"
                    }
                    
                    sh '''
                        source ${VENV_PATH}/bin/activate
                        
                        ${pytestCmd} ${testPath} \
                            -v \
                            --tb=short \
                            --html=${REPORTS_PATH}/report.html \
                            --self-contained-html \
                            --junit-xml=${REPORTS_PATH}/junit.xml \
                            ${parallelOption} \
                            ${markerOption} || true
                        
                        echo "✅ Tests completed"
                    '''
                }
            }
        }

        stage('Generate Reports') {
            steps {
                script {
                    echo "📊 Generating test reports"
                    sh '''
                        source ${VENV_PATH}/bin/activate
                        
                        if [ -f ${REPORTS_PATH}/report.html ]; then
                            echo "✅ HTML report generated"
                            ls -lh ${REPORTS_PATH}/report.html
                        fi
                        
                        if [ -f ${REPORTS_PATH}/junit.xml ]; then
                            echo "✅ JUnit XML report generated"
                            ls -lh ${REPORTS_PATH}/junit.xml
                        fi
                        
                        SCREENSHOT_COUNT=$(find ${REPORTS_PATH}/screenshots -type f -name "*.png" 2>/dev/null | wc -l)
                        echo "📸 Screenshots captured: $SCREENSHOT_COUNT"
                    '''
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                script {
                    echo "📤 Publishing test results"
                    
                    junit(
                        allowEmptyResults: true,
                        testResults: "${REPORTS_PATH}/junit.xml"
                    )
                    
                    publishHTML(
                        reportDir: REPORTS_PATH,
                        reportFiles: 'report.html',
                        reportName: 'pytest HTML Report',
                        keepAll: true,
                        alwaysLinkToLastBuild: true
                    )
                    
                    echo "✅ Test results published"
                }
            }
        }
    }

    post {
        always {
            script {
                echo "🧹 Cleaning up"
                sh '''
                    if [ -f ${REPORTS_PATH}/appium.pid ]; then
                        APPIUM_PID=$(cat ${REPORTS_PATH}/appium.pid)
                        kill $APPIUM_PID 2>/dev/null || true
                    fi
                    pkill -f "appium" || true
                    echo "✅ Cleanup completed"
                '''
            }

            archiveArtifacts(
                artifacts: 'reports/**/*',
                allowEmptyArchive: true,
                onlyIfSuccessful: false
            )
        }

        success {
            script {
                echo "✅ Pipeline completed successfully"
            }
        }

        failure {
            script {
                echo "❌ Pipeline failed"
            }
        }

        unstable {
            script {
                echo "⚠️  Pipeline unstable - some tests may have failed"
            }
        }
    }
}
