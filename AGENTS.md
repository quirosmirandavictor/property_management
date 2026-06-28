# Repository Rules

## Commit Messages

- Write commit messages in English.
- Use a concise summary line in the format `<scope>: <change summary>`.
- After the summary line, leave a blank line and add a flat bullet list using `*` for the main changes included in the commit.
- Keep bullets action-oriented and specific to the committed scope.

Example:

```text
IAM module: Migrations from Django to alembic_SQLAlchemy

* Config alembic and add migrations for IAM module
* Update the README.md with docker documentation
* Add new references on pyproject.toml
* Add database_url to config.py
```