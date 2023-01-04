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

def read_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create player id dataframe")
    # we will parse the list as a string.
    parser.add_argument("--token", type=str, help="The GitHub token")
    args = parser.parse_args()
    return args
  
def pull_request_checker():
    args = read_args()
    if args.token == None or args.token == '':
        print('The action need a GitHub token')
        sys.exit(1)
    
    # Collects GitHub variables.
    repo_name = get_env_var('GITHUB_REPOSITORY')
    github_ref = get_env_var('GITHUB_REF')
    github_event_name = get_env_var('GITHUB_EVENT_NAME')
    
    pr_number = None
    is_labels_check_failing = False
    is_title_check_failing = False
   
    
    # Creates a repository object, using the GitHub token.
    repo = Github(args.token).get_repo(repo_name)
    
    # Gets the pull request number.
    try:
        pr_number = int(re.search('refs/pull/([0-9]+)/merge', github_ref).group(1))
    except AttributeError:
        print('ERROR: The pull request number could not be extracted from 'f'GITHUB_REF = "{github_ref}"', file=sys.stderr)
        sys.exit(1)

    print(f'Pull request number: {pr_number}')
    
    # Create a pull request object
    pr = repo.get_pull(pr_number)
    
    # Get the pull request labels and check if the PR has labels.
    pr_labels = pr.get_labels()
    print(f'Pr labels: {pr_labels.totalCount}')
    if pr_labels.totalCount == 0:
        is_labels_check_failing = True
        pr.create_review(
            body='This pull request has not labels. Please provide at list one labels identifing this pull request.',
            event='REQUEST_CHANGES')
    
    # Checks the title of the pull request.
    pr_title = pr.title
    match = re.search('[^0-9A-Za-z ]', pr_title)
    print(f"Pr title: {pr_title} - Title match -> {match}")
    if match != None:
        is_title_check_failing = True
        pr.create_review(
            body='☠️ The pull request title must be without special characters. Please fix it!',
            event='REQUEST_CHANGES')
    
    # Dimisses the reviews if all the checks pass.
    if is_labels_check_failing == False and is_title_check_failing == False:
        pr_reviews = pr.get_reviews()
        for review in pr_reviews:
            if review.user.login == 'github-actions[bot]':
                if review.state == 'CHANGES_REQUESTED':
                    print(f"Deleting the review id -> {review.id} with user -> {review.user.login} - with state -> {review.state}")
                    review.dismiss('😎 All the PR checks passed, and we dismissed the associated reviews!')
        
    
if __name__ == "__main__":
    pull_request_checker()
