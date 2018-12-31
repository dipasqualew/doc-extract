"""
Fabfile
"""
from fabric.api import local
from fabric.colors import cyan

def _print_block(block_description):
    """
    Prints the block description
    """
    separator = cyan("-" * len(block_description))
    print("")
    print(separator)
    print(cyan(block_description))
    print(separator)
    print("")

def run_pytest():
    """
    Run pytest
    """
    _print_block("Executing unit tests")
    local("coverage run --branch -m pytest")
    generate_coverage_report()

def run_bandit():
    """
    Run bandit
    """
    _print_block("Executing bandit")
    local("bandit doc_extract")

def run_pylint():
    """
    Run pylint
    """
    _print_block("Executing pylint")
    local("pylint doc_extract")

def generate_coverage_report():
    """
    Generates coverage report
    """
    target = "./public/coverage"
    omit = [
        "*test*.py",
        "fabfile.py",
        "docextract**",
    ]
    _print_block("Generating coverage report")
    local(f"coverage html -d {target} --omit={','.join(omit)}")

def test():
    """
    Runs the unit tests
    """
    run_pytest()
    run_bandit()
    run_pylint()
