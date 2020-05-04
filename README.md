# labels

CLI app for managing GitHub labels for Python 3.6 and newer. 📝

## Installation

**labels** is available for download from [PyPI][PyPI] via [pip][pip]:

```text
pip install labels
```

Versions follow [Calendar Versioning][calver] using a `YY.MINOR.MICRO` scheme. 🗓

## Authentication

The labels CLI connects to the GitHub API to modify labels for a GitHub
repository. Please [create your own personal API token][create token] and
choose the correct token scope based on whether you want to manage issue
labels for a public or a private repository. Then set up two environment
variables in your terminal:

```bash
export LABELS_USERNAME="<GITHUB_USERNAME>"
export LABELS_TOKEN="<GITHUB_TOKEN>"
```

## Usage

Once you've installed **labels** and set up the environment variables, you're
ready to use the **labels** CLI to manage labels for a GitHub repository. The
CLI comes with two commands: ``fetch`` and ``sync``. Both commands require
the name of the owner and the name of the GitHub repository to fetch from or
sync to. By default, **labels** tries to load this information from your
local Git repository based on the URL for the `origin` remote repository.

For example, if you run **labels** from your local clone of the [earth
][earth_repo] repository with `origin` set to
`git@github.com:hackebrot/earth.git` owner will be `hackebrot` and repo will
be `earth`. 🌍

You can override one or both of these values manually using the following CLI
options:

```text
-o, --owner TEXT     GitHub owner name
-r, --repo TEXT      GitHub repository name
```

### Fetch

When you use **labels** for the first time, you will start by fetching
information about the existing labels for your GitHub project. The CLI will
then write a [TOML][toml] file to your computer with the retrieved
information. The default name for this file is ``labels.toml`` in your
current working directory and can be changed by passing the ``-f, --filename
PATH`` option followed by the path to where you want to write to.

```text
labels fetch -o hackebrot -r pytest-emoji
```

```toml
[bug]
color = "ea707a"
description = "Bugs and problems with pytest-emoji"
name = "bug"

["code quality"]
color = "fcc4db"
description = "Tasks related to linting, coding style, type checks"
name = "code quality"

[dependencies]
color = "43a2b7"
description = "Tasks related to managing dependencies"
name = "dependencies"

[docs]
color = "2abf88"
description = "Tasks to write and update documentation"
name = "docs"

["good first issue"]
color = "bfdadc"
description = "Tasks to pick up by newcomers to the project"
name = "good first issue"
```

### Sync

Now that you have a file on your computer that represents your GitHub labels,
you can edit this file and then run **labels sync** to update the remote
repository. But first let's look into how that works... 🔍

Representation of a GitHub label in the written TOML file:

```toml
[docs]
color = "2abf88"
description = "Tasks to write and update documentation"
name = "docs"
```

The section name (``[docs]`` in the example above) represents the name of the
label for that repository and is identical to the ``name`` field when running
``labels fetch``. Do not edit the section name of existing labels yourself!

The fields ``color``, ``description`` and ``name`` are parameters that you
can edit with the **labels** CLI.

- ``name`` - The name of the label
- ``description`` - A short description of the label
- ``color`` - The hexadecimal color code for the label without the leading ``#``

You can make the following changes to labels for your repo:

- You can **delete** a label by removing the corresponding section from the
labels file 🗑
- You can **edit** a label by changing the value for one or more parameters for
that label 🎨
- You can **create** a new label by adding a new section with your desired
parameters 📝

When creating labels choose a section name identical to the ``name``
parameter.

Check your label changes before syncing by using the ``dryrun`` CLI option:

```text
-n, --dryrun         Do not modify remote labels
```

Example usage:

```text
labels sync -n -o hackebrot -r pytest-emoji
```

```text
This would delete the following labels:
  - dependencies
This would update the following labels:
  - bug
  - good first issue
This would create the following labels:
  - duplicate
This would NOT modify the following labels:
  - code quality
  - docs
```

Running ``labels sync`` without the ``dryrun`` option also updates the labels
file, so that section names match the ``name`` parameter.

If **labels** encounters any errors while sending requests to the GitHub API,
it will print information about the failure and continue with the next label
until it has processed all of the labels.

## Community

Please check out the [good first issue][good first issue] label for tasks,
that are good candidates for your first contribution to
**labels**. Your contributions are greatly
appreciated! Every little bit helps, and credit will always be given! 👍

Please note that **labels** is released with a [Contributor Code of
Conduct][code of conduct]. By participating in this project you agree to
abide by its terms.

## License

Distributed under the terms of the MIT license, **labels** is free and open
source software.

[PyPI]: https://pypi.org/project/labels/
[calver]: https://calver.org
[code of conduct]: https://github.com/hackebrot/labels/blob/master/CODE_OF_CONDUCT.md
[contributing]: https://github.com/hackebrot/labels/blob/master/.github/CONTRIBUTING.md
[create token]: https://blog.github.com/2013-05-16-personal-api-tokens/
[earth_repo]: https://github.com/hackebrot/earth
[good first issue]: https://github.com/hackebrot/labels/labels/good%20first%20issue
[pip]: https://pypi.org/project/pip/
[toml]: https://github.com/toml-lang/toml
