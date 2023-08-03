# Custom API + E2E Test Automation Framework


## NOTE:
this framework is dockerized, so to run it you need to have Docker server installed 

Setup:

1. Clone the git repo to local folder
2. Navigate to this folder
3. Build docker container by running: docker build -t custom_framework .
4. Run docker image by: docker run -it --rm --ipc=host -p 8888:8080 custom_framework
5. Observe test run results at: http://localhost:8888
