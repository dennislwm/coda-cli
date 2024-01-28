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
- [Introduction](#introduction)
  - [Purpose](#purpose)
  - [Audience](#audience)
- [System Overview](#system-overview)
  - [Benefits and Values](#benefits-and-values)
  - [Workflow](#workflow)
  - [Place, Affordance, Connection](#place-affordance-connection)
  - [Limitation](#limitation)
- [User Personas](#user-personas)
  - [RACI Matrix](#raci-matrix)
- [Requirements](#requirements)
  - [Local workstation](#local-workstation)
- [Usage](#usage)
  - [Running coda-cli in your terminal](#running-coda-cli-in-your-terminal)
- [Shaping](#shaping)
  - [Creating a single CLI command](#creating-a-single-cli-command)
  - [Creating test cases for each command](#creating-test-cases-for-each-command)
  - [Creating a Dockerfile and testing it locally](#creating-a-dockerfile-and-testing-it-locally)
  - [Requiring status checks to pass before merging PR](#requiring-status-checks-to-pass-before-merging-pr)
  - [Building, testing, tagging and uploading our app image using CI](#building-testing-tagging-and-uploading-our-app-image-using-ci)
- [Building](#building)
  - [Building and testing a command and return its output](#building-and-testing-a-command-and-return-its-output)
- [Troubleshooting and FAQs](#troubleshooting-and-faqs)
  - [Error *The following signatures couldn't be verified because the public key is not available*](#error-the-following-signatures-couldnt-be-verified-because-the-public-key-is-not-available)
- [References](#references)
  - [Things to learn and research](#things-to-learn-and-research)

<!-- /TOC -->

---
# 1. Introduction
## 1.1. Purpose

This document describes the `coda-cli` command-line wrapper for Coda.io API, an SaaS service that provides interactive documents similar to Notion, and Google Docs.

## 1.2. Audience

The audience for this document includes:

* User who will create and maintain YAML config files to deploy Coda documents using the CLI.

* DevSecOps Engineer who will develop the CLI, create unit tests, configure build tools, create and maintain continuous integration and deployment (CI/CD) pipelines, and write documentation.

---
# 2. System Overview
## 2.1. Benefits and Values

1. Currently, creating a Coda document requires the User to navigate the Coda user interface (UI) and perform click operations, which may be inefficient and error prone.

2. This CLI allows the User to create and maintain YAML config files that defines a Coda document as code, hence reducing the error rate, while increasing reusability and adding version control for a document as code.

## 2.2. Workflow

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

## 2.3. Place, Affordance, Connection

* Places users can navigate
  * Circle CI `https://app.circleci.com/settings/project/github/dennislwm/coda-cli`
  * GitLab CD `https://gitlab.com`
  * Docker Hub e.g. `https://hub.docker.com/repository/docker/dennislwm/coda-cli`

* Affordance users can act
  * Docker pull `docker pull dennislwm/coda-cli:latest`

## 2.4. Limitation

* The CD pipeline is currently blocked, because Coda.io API does not support POST requests for many of its resources.

---
# 3. User Personas
## 3.1 RACI Matrix

| Category |                            Activity                             | User | DevSecOps |
|:--------:|:---------------------------------------------------------------:|:----:|:---------:|
|  Usage   |               Running `coda-cli` in your terminal               | R,A  |           |
| Shaping  |                  Creating a single CLI command                  |      |    R,A    |
| Shaping  |              Creating test cases for each command               |      |    R,A    |
| Shaping  |          Creating a Dockerfile and testing it locally           |      |    R,A    |
| Shaping  |        Requiring status checks to pass before merging PR        |      |    R,A    |
| Shaping  | Building, testing, tagging and uploading our app image using CI |      |    R,A    |
| Building |      Building and testing a command and return its output       |      |    R,A    |

---
# 4. Requirements
## 4.1. Local workstation

Before running the Python app on your local workstation, you need the following:

- Generate a [CODA_API_KEY](https://coda.io) and save it in an `.env` file, or run the command `export CODA_API_KEY=<CODA_API_KEY>`
- Download and install [jq](https://stedolan.github.io/jq/download/) command line application.
- Install Python dependencies in a virtual environment within the `app` folder with `pipenv shell && make install_new`.

---
# 5. Usage

## 5.1. Running `coda-cli` in your terminal

```sh
python coda.py
Usage: coda.py [OPTIONS] COMMAND [ARGS]...

  This script prints coda data

Options:
  --version                       Show the version and exit.
  -o, --out [csv|json|markdown|text]
                                  Output type, default=text
  -h, --help                      Show this message and exit.

Commands:
  list-docs      Returns the list of documents in Coda
  list-sections  Returns the list of sections in a doc
  list-tables    Returns the list of tables in a doc
```

---
# 6. Shaping

As shaping and building have independent cycles, we will define shaping as any work that does not involve implementation of code. This work may include evaluation, feasibility, comparison, research, etc.

We set a time constraint of 9 workdays, for shaping, and an additional 9 workdays for building. Hence, the total time for this project is approximately 20 workdays with a cool-down of 2 workdays.

## 6.1. Creating a single CLI command

- [X] [Create a single CLI command with Python](doc/shape01.md#create-a-single-cli-command-with-python)
  - [Create a virtual environment](doc/shape01.md#create-a-virtual-environment)
  - [Install dependencies](doc/shape01.md#install-dependencies)
  - [Create a Makefile](doc/shape01.md#create-a-makefile)
  - [Create a Main Application](doc/shape01.md#create-a-main-application)

## 6.2. Creating test cases for each command

- [X] [Create test cases for each command with Python](doc/shape02.md#create-test-cases-for-each-command-with-python)
  - [Test Driven Development](doc/shape02.md#test-driven-development)
  - [Install developer dependencies](doc/shape02.md#install-developer-dependencies)
  - [Create a test file](doc/shape02.md#create-a-test-file)

## 6.3. Creating a Dockerfile and testing it locally

- [X] [Create a Dockerfile and test it locally](doc/shape03.md#create-a-dockerfile-and-test-it-locally)
  - [Create a Dockerfile](doc/shape03.md#create-a-dockerfile)
  - [Generate a requirements file](doc/shape03.md#generate-a-requirements-file)

## 6.4. Requiring status checks to pass before merging PR

- [X] [Require status checks to pass before merging PR](doc/shape04.md#require-status-checks-to-pass-before-merging-pr)
  - [Status Checks](doc/shape04.md#status-checks)
  - [Continuous Integration](doc/shape04.md#continuous-integration)

## 6.5. Building, testing, tagging and uploading our app image using CI

- [X] [Build, test, tag and upload our app image using CI](doc/shape05.md##build-test-tag-and-upload-our-app-image-using-ci)
  - [Workflows](doc/shape05.md#workflows)
  - [Sequential job execution with dependency](doc/shape05.md#sequential-job-execution-with-dependency)
  - [Create an access token for Docker Hub](doc/shape05.md#create-an-access-token-for-docker-hub)

The project started on 17-Aug-2022 and is currently a work-in-progress and ahead of schedule. The shaping cycle was completed on 19-Aug-2022 (2 days), while the building cycle is in progress.

> Note: All the `list-*` commands have been implemented and tested.

---
# 7. Building
## 7.1. Building and testing a command and return its output

This steps are repeatable, i.e. create and test a command.

- [ ] [Build and test a command and return its output](doc/build01.md#build-and-test-a-command-and-return-its-output)
  - [Test driven development of a command](doc/build01.md#test-driven-development-of-a-command)
  - [Create test case](doc/build01.md#create-test-case)
  - [Configure build](doc/build01.md#configure-build)
  - [Build the command](doc/build01.md#build-the-command)

---
# 9. Troubleshooting and FAQs
## 9.1. Error *The following signatures couldn't be verified because the public key is not available*

Context Analysis:
* Project: `coda-cli`
* CI Workflow: `static-analysis-workflow`
* CI Job: `static-analysis`
* CI Step: Build image
* CI Last Command: `cd app && make ci_test_build`
* CI Output:

```sh
 => ERROR [2/7] RUN apt-get update                                         0.5s
------
 > [2/7] RUN apt-get update:
#5 0.263 Get:1 http://deb.debian.org/debian bookworm InRelease [151 kB]
#5 0.270 Get:2 http://deb.debian.org/debian bookworm-updates InRelease [52.1 kB]
#5 0.271 Get:3 http://deb.debian.org/debian-security bookworm-security InRelease [48.0 kB]
#5 0.301 Err:1 http://deb.debian.org/debian bookworm InRelease
#5 0.301   The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 0E98404D386FA1D9 NO_PUBKEY 6ED0E7B82643E131 NO_PUBKEY F8D2585B8783D481
```

Problem Analysis:
1. The `docker build` command fails on the second layer, i.e. `RUN apt-get update`, with error `The following signatures couldn't be verified because the public key is not available`.
2. [StackOverflow](https://stackoverflow.com/questions/73699753/the-following-signatures-couldnt-be-verified-because-the-public-key-is-not-avai) top answer recommends upgrading the docker on the host.
3. [CircleCI documentation](https://circleci.com/docs/building-docker-images/#docker-version) suggests possible docker versions:
  * `default` - set to latest Docker 24.
  * `docker23` - set to previous Docker 23.
  * `20.10.24` - specific Docker version.
4. The custom CI config `.circleci/config.yml` has an older docker version, i.e. `19.03.13`, used in both `static-analysis` and `deploy-image` jobs.
5. The solution appears to be updating the docker version to `default`.

---
# 8. References
## 8.1. Things to learn and research

In no particular order, my plan is to use the following resources to learn and research.

| Title | Author | Publisher Date [Short Code]
|---|---|---|
| E-Book: Shape Up | Ryan Singer | Basecamp 2021
| GitHub Repo: [Blasterai/codaio](https://github.com/Blasterai/codaio) | BlasterAI | 2022
| E-Doc: [Click](https://click.palletsprojects.com) | Pallets | 2022
| GitHub Repo: [dennislwm/archiveso](https://github.com/dennislwm/archiveso) | Dennis Lee | 2022

