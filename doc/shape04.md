# Require status checks to pass before merging PR

<!-- TOC -->

- [Require status checks to pass before merging PR](#require-status-checks-to-pass-before-merging-pr)
- [Constraint](#constraint)
  - [Hill chart](#hill-chart)
- [Place, Affordance, Connection](#place-affordance-connection)
- [Status Checks](#status-checks)
- [Continuous Integration](#continuous-integration)

<!-- /TOC -->

# Constraint

Base time: 2 workday (Max: 4)

## Hill chart
```
  .
 . .
.   +
0-1-2
```

# Place, Affordance, Connection

# Status Checks

1. We will use the python package `prospector` to perform static analysis. 

Edit the file `Makefile` and the following code:

```makefile
...
ci_build: ci_freeze
	DOCKER_BUILDKIT=1 docker build -t coda-cli .

ci_freeze:
  pip3 install pipreqs
	pipreqs --ignore tests . --force
	echo "prospector==1.6.0" >> ./requirements.txt
	pip3 uninstall -y pipreqs
```

Each time you run `make ci_build`, the `ci_freeze` dependency is executed. The package `prospector` is not included in the `Pipfile` because the application doesn't require it.

2. We will use `docker-compose` in our CI pipeline, with a `prospector` entrypoint that executes the static analysis.

Create a file `docker-compose.yml` file in the path `app/` and enter the following:

```yml
version: '3.7'

services:
  # Pipeline actions
  prospector:
    image: coda-cli:latest
    entrypoint: /usr/local/bin/prospector
```

> Note: As the `docker-compose.yml` file depends on our custom image `coda-cli:latest`, we need to ensure that `make ci_build` gets executed before it in our CI pipeline.

# Continuous Integration

CircleCI ["CCI"] has a free plan that includes 30,000 free credits per month (or 6,000 build minutes per month).

<details>
  <summary>Configure CircleCI to check GitHub status.</summary><br>

1. Add your GitHub repo to CCI.

Navigate to [CCI web page](https://circleci.com) and login with your GitHub credentials.

Select **Organization Settings** --> **VCS** --> **Manage GitHub Checks**.

Select which repo you want to utilize checks and click the **Install** button.

2. Create a file `.config.yml` in the `.circleci/` folder of your repo. Add the following lines to the file:

```yml
# Use the latest 2.1 version of CircleCI pipeline process engine.
# See: https://circleci.com/docs/2.0/configuration-reference
version: 2.1

# Define a job to be invoked later in a workflow.
# See: https://circleci.com/docs/2.0/configuration-reference/#jobs
    # Specify the execution environment. You can specify an image from Dockerhub or use one of our Convenience Images from CircleCI's Developer Hub.
    # See: https://circleci.com/docs/2.0/configuration-reference/#docker-machine-macos-windows-executor
    # Add steps to the job
    # See: https://circleci.com/docs/2.0/configuration-reference/#steps
    # working_directory (Default: /home/circleci/project)
    #   root folder of repo
jobs:
  static-analysis:
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
          name: "Run static analysis"
          command: cd app && docker-compose up -d

# Invoke jobs via workflows
# See: https://circleci.com/docs/2.0/configuration-reference/#workflows
workflows:
  static-analysis-workflow:
    jobs:
      - static-analysis
```

The root of our repo is initially checked out to the default working directory `/home/circleci/project`. The step `setup_remote_docker` adds support for `docker-compose` and Docker BuildKit.

The first `run` builds our custom Docker image, while the second `run` executes the `docker-compose.yml` that performs the static-analysis.

3. To take full advantage of our configured CI system, we need to ensure that we check the build before merging it into the main branch.

Navigate to your GitHub repo, and click on the repo **Settings** --> **Branches** --> **Add Rule**. 

- In field **Branch name pattern**, enter `main`.
- Under **Protect matching branches** section:
  - Enable checkbox **Require a pull request before merging**
  - Enable checkbox **Require status checks to pass before merging** 
    - Enable checkbox **Require branches to be up to date before merging**
  - Enable checkbox **Require linear history**
- In the search box, type `ci`. Select the checks that are required.
- Click **Save changes** button.
</details>

Each time you make a PR for your repo, CCI automatically runs your `config.yml` file. If any steps fail, then you will not be able to merge your PR with the `main` branch.
