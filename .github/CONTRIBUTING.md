# Contributing


Thank you for taking the time to contribute to this project!


## Code of Conduct

This project adheres to the Contributor Covenant (see [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md)).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to qwikidata-maintainer@kensho.com.


## Contributor License Agreement

Each contributor is required to agree to our Contributor License Agreement, to ensure that their contribution may be safely merged into the project codebase and released under the existing code license. This agreement does not change contributors' rights to use the contributions for any other purpose -- it is simply used for the protection of both the contributors and the project.


## Guide


To develop you should fork and clone the repo.  Then you can pip install it for local development,

```bash
pip install -e ".[dev]"
```

We use the [pre-commit](https://github.com/pre-commit/pre-commit) package to handle code style.  You can see the list of pre-commit hooks in the top level ``.pre-commit-config.yaml`` file. The pre-commit package will be installed when you specify the ``dev`` extra requirement as above. The first time you do this, you will need to install the pre-commit hooks.  **NOTE:** If you are using conda you should ``conda install virtualenv`` so that ``pre-commit`` has a version it can use.

```bash
pre-commit install --install-hooks
```

Once your commits pass the pre-commit checks you can open a pull request.
