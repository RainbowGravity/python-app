# Web application on Python

## About

This application was created as part of the DevOps exam. Application is very simple and replies only with "Hello World 1" message. As for the Docker image homework this application is using the Gunicorn server integrated.

More interesting thing is a Github flow workflow created for deployment of this app.

## About Gitflow

Gitflow is a very complicated workflow with several long-live branches. There are Hotfix, Release, Develop and Main branches. State of the project is storing in these branches. 

Every developer is workin in his own feature branch. Developer commiting in his own branch with new versions of feature with reasonable commit messages. Commit messages allows to check development history and roll back the changes if critical issue was found. 

After feature is complete developer creating a pull request for merging his branch into develop branch. After the pull request is opened code reviewing and conversations are started. Developer is in process of updating and improvement of his code. If everyone is desided that code is complete, then pull request is applied and feature branch is deleted. 

But it is not over yet. Before merging to the main branch there is a Release branch. Only after merging Develop branch with the Release branch code will be able to merge with the Main. 

This workflow was created and popularised in 2010 year. But Gitflow is actual even now for low commit rate projects which are requires for clear history and versionning.

## My implementation of this process

My implementation is based on Github Actions and its workflows. Each workflow can be described by the .yml/.yaml file and can be triggered by many events: pull requests, pushes, merges, issues, etc. 

My workflow works like this:

* At first we need a running infrastructure. Infrustructure creation can be triggered by [Run Infrustrictire](https://github.com/RainbowGravity/python-app/actions/workflows/run_infrastructure.yml) Github workflow. After process is complete we are ready to go.
* Then we need to create a pull request with the new code version. After this automated code tests will run. In Python case: dockerfilelint, mypy, pylint, Snyk test, Snyk code test. Results of the code checks will be posted as comment for the PR and automatically will be sent to my Telegram and Email. 
* If everything is OK and code is ready to merge, then pull request will be closed and feature branch will be merged to the dev. 
* When code is pushed to the dev, then code docker image building process is started. After successfully code building container will be pushed to the ECR golang-app-dev repository with a unique tag that is commit hash.
* Then Terraform will do its part: create a Dev ECS Service, tasks definition, target group and 9090 port listener. Now service can be accessed by the 9090 port of the ALB.
* After merging to the dev branch from feature we need to create another pull request for merging with the main branch. Process was simplified for the demonstration.  
* Then the same process as for Dev will be started for the Blue and Green ECS Services. But each deployment of them requied a review and approval. e.g. It allows to change traffic between Blue and Green by [Redirect Traffic](https://github.com/RainbowGravity/python-app/actions/workflows/redirect_traffic.yml) Github workflow.
* After process is complete [automated workflow](https://github.com/RainbowGravity/python-app/actions/workflows/destroy_gruen.yml) of redirecting a traffic back to Blue and destroying the Green is started. New service is the Blue one now.

<p align=center><b>Workflow diagram</b></p>
<p align=center>

  <img width="800" height="407" src="https://user-images.githubusercontent.com/89798605/138299972-5619cbf8-e83f-4e0d-a984-dd5984b2f059.png">

 
</p>
