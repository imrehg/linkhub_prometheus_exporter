import nox

source_folders = ["src/"]
project_folders = source_folders + ["tests/"]

# Default sessions
nox.options.sessions = ["lint", "test"]


@nox.session
def format(session):
    """Run code formatting."""
    session.run("poetry", "install", external=True)
    session.run("isort", *project_folders)
    session.run("black", *project_folders)


@nox.session
def lint(session):
    """Run linting checks on the code."""
    session.run("poetry", "install", "--with", "test", external=True)
    session.run("isort", "--check", *project_folders)
    session.run("black", "--check", *project_folders)
    session.run("flake8", *project_folders)
    session.run("mypy", *source_folders)
    session.run("bandit", "-r", *source_folders)


@nox.session(python=["3.10", "3.11"])
def test(session):
    """Run tests on the code."""
    session.run("poetry", "install", "--with", "test", external=True)
    try:
        session.run("coverage", "run", "-m", "pytest")
    finally:
        session.run("coverage", "report", "-m")
