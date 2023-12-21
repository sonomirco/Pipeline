import os
import sys
import re
import argparse
import distutils.util
from github import Github

def get_env_var(env_var_name, echo_value=True):
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
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read PR")
    # we will parse the list as a string.
    parser.add_argument("--token", type=str, help="The GitHub token")
    parser.add_argument("--pr_number", type=str, help="pr number")
    args = parser.parse_args()
    return args
  
def pull_request_checker():
    if args.token == None or args.token == '':
        print('The action need a GitHub token')
        sys.exit(1)
    
    # Collects GitHub variables.
    repo_name = get_env_var('GITHUB_REPOSITORY')

    # Creates a repository object, using the GitHub token.
    repo = Github(args.token).get_repo(repo_name)
    pr_number = int(args.pr_number)
    pr = repo.get_pull(pr_number)
    
    # Get the pull request labels and check if the PR has labels.
    pr_labels = pr.get_labels()
    print(f'Pr labels: {pr_labels.totalCount}')

if __name__ == "__main__":
    args = parse_arguments()
    try:
        result = pull_request_checklist(args.token, args.pr_number)
        print(result)
    except ValueError as e:
        print(e)
        sys.exit(1)
