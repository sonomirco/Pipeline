import os
import sys
import re
import argparse
import distutils.util
from github import Github

def get_env_var(env_var_name, echo_value=False):
    """Try to get the value from a environmental variable.
    If the values is 'None', then a ValueError exception will
    be thrown.
    Args
    ----
    env_var_name : str
        The name of the environmental variable.
    echo_value : bool, optional, default False
        Print the resulting value.
    Returns
    -------
    value : str
        The value from the environmental variable.
    """
    value = os.getenv(env_var_name)

    if value is None:
        print(f'ERROR: The environmental variable {env_var_name} is empty!',
              file=sys.stderr)
        sys.exit(1)

    if echo_value:
        print(f"{env_var_name} = {value}")

    return value

def read_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create player id dataframe")
    # we will parse the list as a string.
    parser.add_argument("--token", type=str, help="The GitHub token")
    parser.add_argument("--valid_labels", type=str, help="The valid labels")
    
    args = parser.parse_args()
    return args
  
def check_pr():
    args = read_args()
    print(f"inputs -> {args.token} - type -> {type(args.token)}")
    
    valid_labels = [label.strip() for label in args.valid_labels.split(',')]
    print(f'Valid labels are: {valid_labels}')
    
    repo_name = get_env_var('GITHUB_REPOSITORY')
    github_ref = get_env_var('GITHUB_REF')
    github_event_name = get_env_var('GITHUB_EVENT_NAME')
    pr_number = None
    
    print(f"repo name -> {repo_name} - ref -> {github_ref} - event -> {github_event_name}")
    
    # Create a repository object, using the GitHub token
    repo = Github(args.token).get_repo(repo_name)
    
    try:
        pr_number = int(re.search('refs/pull/([0-9]+)/merge', github_ref).group(1))
    except AttributeError:
        print('ERROR: The pull request number could not be extracted from 'f'GITHUB_REF = "{github_ref}"', file=sys.stderr)
        sys.exit(1)

    print(f'Pull request number: {pr_number}')
    
    # Create a pull request object
    pr = repo.get_pull(pr_number)
    
    # Get the pull request labels
    pr_labels = pr.get_labels()
    print(f'Pr labels: {len(pr_labels)}')
    
if __name__ == "__main__":
    check_pr()
