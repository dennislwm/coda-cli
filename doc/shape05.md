# Build, test, tag and upload our app image using CI

<!-- TOC -->

- [Build, test, tag and upload our app image using CI](#build-test-tag-and-upload-our-app-image-using-ci)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Workflows](#workflows)
- [Sequential job execution with dependency](#sequential-job-execution-with-dependency)
- [Create an access token for Docker Hub](#create-an-access-token-for-docker-hub)

<!-- /TOC -->

# Constraint

Base time: 1 workday (Max: 2)

## Hill chart
```
 .
. +
0-1
```

# Place, Affordance, Connection

* Places users can navigate
  * Docker Hub e.g. `https://hub.docker.com/repository/docker/dennislwm/coda-cli`
  
* Affordance users can act
  * Docker pull `docker pull dennislwm/coda-cli:latest`

# Workflows

A workflow is a set of rules for defining a collection of jobs and their run order. Workflows support complex job orchestration using a simple set of configuration keys to help you resolve failures sooner.

Ideally, when a push is made to a feature branch we want to run `static-analysis` job to test source code, then when a pull request is merged to the main branch we want to run `deploy-image` job to push an image to an artifactory, i.e. Docker Hub.

However, in our shaping phase, we simplify this process by combining both jobs such that if the `static-analysis` job passes, we immediately run `deploy-image` job. During our building phase, we should implement a separate trigger for the latter job.

# Sequential job execution with dependency

Jobs in a workflow are isolated from each other, the image we built on the `static-analysis` job is not available to `deploy-image`. From CircleCI version 2.1, we can reuse some configurations directly by specifying a reusable `executor`, while `persist_to_workspace` can persist a file between jobs.

1. Edit file `.config.yml` in the `.circleci/` folder of your repo. Add the following lines to the end of file under `workflows`:

```yml
workflows:
  static-analysis-workflow:
    jobs:
      ...
      - deploy-image:
          requires:
            - static-analysis
```

2. In the same file, add the following lines under `jobs`:

```yml
jobs:
...
  deploy-image:
    docker:
      - image: cimg/python:3.9.10
    steps:
      - checkout
      - setup_remote_docker:
          version: 19.03.13
      - run:
          name: "Build image"
          command: cd app && make ci_build
      - run:
          name: "Publish image to Docker Hub"
          command: |
              echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
              docker tag coda-cli:latest $DOCKERHUB_USERNAME/coda-cli:latest
              docker push $DOCKERHUB_USERNAME/coda-cli:latest
```

3. We need to create new CircleCI environment variables with our Docker Hub username and personal access token. If multiple projects are going to push images to Docker Hub, the recommended way is to use **Contexts**.

For this project, we will set them directly in the **Project Settings**. Add Environment Variable for each of the following:

`DOCKERHUB_USERNAME`: `USERNAME`
`DOCKERHUB_PASS`: `PERSONAL_ACCESS_TOKEN`

# Create an access token for Docker Hub

Log in to [hub.docker.com](https://hub.docker.com/).

Click on your username in the top right corner and select **Account Settings**.

Select [Security](https://hub.docker.com/settings/security) -> **New Access Token**.

**Access Token Description**: `circleci-coda-cli`
**Access permissions**: `Read, Write, Delete`

Click **Generate** button, then copy your `PERSONAL_ACCESS_TOKEN`.