# coda-cli

<!--- See https://shields.io for others or to customize this set of shields.  --->

![Docker Pulls](https://img.shields.io/docker/pulls/dennislwm/coda-cli.svg)
![Docker Build](https://img.shields.io/docker/image-size/dennislwm/coda-cli.svg)
![Docker Build](https://img.shields.io/docker/v/dennislwm/coda-cli.svg)
[![dennislwm](https://circleci.com/gh/dennislwm/coda-cli.svg?style=shield)](https://app.circleci.com/pipelines/github/dennislwm/coda-cli)
![GitHub last commit](https://img.shields.io/github/last-commit/dennislwm/coda-cli?color=red&style=plastic)

This application is a Python CLI that interacts with Coda.io, which is a SaaS. This project consist of (1) python CLI; (2) CI pipeline that automates your static analysis and image deployment; and (3) CD pipeline to deploy a custom Docker image that interacts with Coda.io (Blocked).

<!-- TOC -->

- [coda-cli](#coda-cli)
- [Overview](#overview)
- [Things to learn and research](#things-to-learn-and-research)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Workflow](#workflow)
- [Usage](#usage)
  - [Prerequisites](#prerequisites)
  - [Run Coda](#run-coda)
- [Shaping](#shaping)
- [Building](#building)
- [Limitation](#limitation)

<!-- /TOC -->

---
# Overview

![Overview](img/overview.png)

---
# Things to learn and research

In no particular order, my plan is to use the following resources to learn and research. 

| Title | Author | Publisher Date [Short Code]
|---|---|---|
| E-Book: Shape Up | Ryan Singer | Basecamp 2021
| GitHub Repo: [Blasterai/codaio](https://github.com/Blasterai/codaio) | BlasterAI | 2022
| E-Doc: [Click](https://click.palletsprojects.com) | Pallets | 2022
| GitHub Repo: [dennislwm/archiveso](https://github.com/dennislwm/archiveso) | Dennis Lee | 2022

# Place, Affordance, Connection

* Places users can navigate
  * Circle CI `https://app.circleci.com/settings/project/github/dennislwm/coda-cli`
  * GitLab CD `https://gitlab.com` 
  * Docker Hub e.g. `https://hub.docker.com/repository/docker/dennislwm/coda-cli`
  
* Affordance users can act
  * Docker pull `docker pull dennislwm/coda-cli:latest`

---
# Workflow

This project uses several methods and products to optimize your workflow.
- Use a version control system (**GitHub**) to track your changes and collaborate with others.
- Use a static analyzer (**prospector**) to help write your clean code.
- Use a build tool (**Makefile**) to automate your development tasks.
- Use a package manager (**Pipenv**) to manage your dependencies.
- Use a testing framework (**pytest** and **click.testing**) to automate your testing.
- Use a containerization platform (**Docker**) to run your application in any environment.
- Use a continuous integration pipeline (**CircleCI**) to automate your static analysis and image deployment.
- Use an artifactory (**Docker Hub**) to store and pull your image.
- Use a continuous delivery pipeline (**GitLab**) to automate your Docker container deployment and interaction with Coda.io (Blocked: Coda.io doesn't support POST request for many of its resources.)

---
# Usage

## Prerequisites

Before running the Python app on your local workstation, you need the following:

- Generate a [CODA_API_KEY](https://coda.io) and save it in an `.env` file.
- Download and install [jq](https://stedolan.github.io/jq/download/) command line application.
- Install Python dependencies in a virtual environment within the `app` folder with `pipenv shell && make install_new`.

## Run Coda

```sh
python coda.py
```

---
# Shaping

As shaping and building have independent cycles, we will define shaping as any work that does not involve implementation of code. This work may include evaluation, feasibility, comparison, research, etc.

We set a time constraint of 9 workdays, for shaping, and an additional 9 workdays for building. Hence, the total time for this project is approximately 20 workdays with a cool-down of 2 workdays.

- [X] [Create a single CLI command with Python](doc/shape01.md#create-a-single-cli-command-with-python)
  - [Create a virtual environment](doc/shape01.md#create-a-virtual-environment)
  - [Install dependencies](doc/shape01.md#install-dependencies)
  - [Create a Makefile](doc/shape01.md#create-a-makefile)
  - [Create a Main Application](doc/shape01.md#create-a-main-application)
- [X] [Create test cases for each command with Python](doc/shape02.md#create-test-cases-for-each-command-with-python)
  - [Test Driven Development](doc/shape02.md#test-driven-development)
  - [Install developer dependencies](doc/shape02.md#install-developer-dependencies)
  - [Create a test file](doc/shape02.md#create-a-test-file)
- [X] [Create a Dockerfile and test it locally](doc/shape03.md#create-a-dockerfile-and-test-it-locally)
  - [Create a Dockerfile](doc/shape03.md#create-a-dockerfile)
  - [Generate a requirements file](doc/shape03.md#generate-a-requirements-file)
- [X] [Require status checks to pass before merging PR](doc/shape04.md#require-status-checks-to-pass-before-merging-pr)
  - [Status Checks](doc/shape04.md#status-checks)
  - [Continuous Integration](doc/shape04.md#continuous-integration)
- [X] [Build, test, tag and upload our app image using CI](doc/shape05.md##build-test-tag-and-upload-our-app-image-using-ci)
  - [Workflows](doc/shape05.md#workflows)
  - [Sequential job execution with dependency](doc/shape05.md#sequential-job-execution-with-dependency)
  - [Create an access token for Docker Hub](doc/shape05.md#create-an-access-token-for-docker-hub)

The project started on 17-Aug-2022 and is currently a work-in-progress and ahead of schedule. The shaping cycle was completed on 19-Aug-2022 (2 days), while the building cycle is in progress.

---
# Building

This steps are repeatable, i.e. create and test a command.

- [ ] [Build and test a command and return its output](doc/build01.md#build-and-test-a-command-and-return-its-output)
  - [Test driven development of a command](doc/build01.md#test-driven-development-of-a-command)
  - [Create test case](doc/build01.md#create-test-case)
  - [Configure build](doc/build01.md#configure-build)
  - [Build the command](doc/build01.md#build-the-command)

---
# Limitation

* The CD pipeline is currently blocked, because Coda.io API does not support POST requests for many of its resources. 
