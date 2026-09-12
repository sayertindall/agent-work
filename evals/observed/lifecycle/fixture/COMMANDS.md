# `fixture-cli` command reference

Run the fixture from the work repository root with `python3 fixture/cli.py`.
The public commands are `list` and `show`.

## `list`

List the available record IDs. The command takes no arguments.

```text
$ python3 fixture/cli.py list
alpha
beta
```

## `show <record_id>`

Display one record by its ID.

```text
$ python3 fixture/cli.py show beta
beta: Second fixture record
```

The available IDs can be obtained with `list`.
