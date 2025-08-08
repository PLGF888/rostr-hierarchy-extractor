# test-selenium-hierarchie

[![Made With Love](https://img.shields.io/badge/Made%20With-Love-orange.svg?style=for-the-badge)](https://github.com/chetanraj/awesome-github-badges) ![py_version](https://img.shields.io/badge/python-^3.11-blue?style=for-the-badge&logo=python&logoColor=9cf) ![version](https://img.shields.io/badge/version-0.1.0-gree?style=for-the-badge&logo=semver) ![code quality](https://img.shields.io/badge/code_quality-A-51C62B?style=for-the-badge&logo=codeforces&logoColor=9cf)

## 📖 Context

Welcome to the test-selenium-hierarchie project. This repository contains everything you need to quickly set up your Python development environment using UV.

## 🚀 Get Started

You can download Python from the [official website](https://www.python.org/downloads/) (**version 3.11 or higher is recommended**).

> ⚠️ **Important:** You can install all the system requirements for the development environment workflow, you can use the `setup_dev.bat` script to ensure all the requirements installation.

Once python installed, you need to clone the project from GitHub,

```sh
git clone <repo-url>
cd test-selenium-hierarchie
```

you can use `pip` to install packages or just use `UV`. UV is recommended for more efficient and more organized than using pip.

``` sh
UV sync # (recommended for devs)
# or, you can also use the quick setup script
.\setup.bat
```

Once the packages are installed, you can refer to the Makefile for all the necessary commands:
  
- **bake**: Init a UV env and installing some useful packages (run this first).
- **clean**: Delete unwanted files
- **cloc**: Count blank lines, comment lines, and physical lines of source code
- **format**: Format the source code using black and Ruff
- **lock**: Generate `uv.lock` file for dependencies
- **mypy**: Run mypy for data type check
- **quality**: Compute various metrics from the source code (code quality)
- **reqs**: Generate requirements.txt file for dependencies
- **run**: Execute the project's main script (main.py)

**P.S:** You can install `make` on Windows using Scoop or just copy paste the commands from file and execute them in the terminal.

## 🌳 Workflow & Pipeline

### 🌱 Branching & Versioning

Before presenting the different branches, we need to present the environments where our code is gonna be deployed:

- **development:** the process where the code is developed, updated and tested frequently. Nothing done in the development environment affects what users currently see. This is just for the devs to see how new features will work and try out improvements.
- **staging:** the stage environment is as similar to the production environment as it can be.
- **prod:** this is the environment where your project will live. This is where users will access the final code after all the updates and testing.

Branches can be created anytime we want, but we define few branches with fixed names to be references depending on the environment we are deploying to:

- **main:** the main’s branch content is deployed to the **staging environment**, once the code is tested and approved to production, we just add a **git tag** (a release) to be deployed to the **production environment**,
- **develop:** development branch where the content is deployed to the development environment,
- **feat/{branch_name}:** a branch with the goal to add new feature to our code,
- **fix/{branch_name}:** a branch with the goal to fix a bug after deploying a feature.

The release version follows the norms of [semantic versioning](https://semver.org/). For example, the git tag naming convention is like **v0.1.0** Given a version number `MAJOR.MINOR.PATCH`, we increment the:

- **MAJOR** version when you make incompatible API changes,
- **MINOR** version when you add functionality in a backwards compatible manner,
- **PATCH** version when you make backwards compatible bug fixes.

### 📜 Conventional commits

To keep the commit history explicit, clean and organized, it's interesting to follow a set of rules that define a lightweight convention on top of commit messages. Inspired by [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/), a commit message should be structured as follows:

``` sh
<type>[optional scope]: <description>
[optional body]
[optional footer(s)]
```

The `<type>` describes the commit type and takes the following values:

``` sh
- :feat:          feat: a new feature
- :fix:           fix: a bug fix
- :docs:          docs: documentation only changes
- :style:         style: changes that do not affect the meaning of the code
                  (white-space, formatting, missing semi-colons, etc)
- :refactor:      refactor: a code change that neither fixes a bug nor adds a feature
- :perf:          perf: a code change that improves performance
- :test:          test: adding missing or correcting existing tests
- :chore:         chore: changes to the build process or auxiliary 
                  tools and libraries such as documentation generation
- :chore-release: chore(release): code deployment or publishing to external repositories
- :chore-deps:    chore(deps): add or delete dependencies
- :build:         build: changes related to build processes
- :ci:            ci: updates to the continuous integration system
- :config:        config: Changing configuration files.
- :security:      security: Fixing security issues.
```

## 🤝 Contribution

- Create a branch (`git checkout -b feat/my-feature`)
- Make your modifications
- Check your changes (`make format`, `make quality`, `make mypy`)
- Create a detailed Pull Request
