import os
import sys
import re
import argparse
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
    # We will parse the list as a string.
    parser.add_argument("--token", type=str, help="The GitHub token")
    args = parser.parse_args()
    return args

def get_pr_number(github_ref: str):
    pr_number = None
    try:
        pr_number = int(re.search('refs/pull/([0-9]+)/merge', github_ref).group(1))
    except AttributeError:
        print('ERROR: The pull request number could not be extracted from 'f'GITHUB_REF = "{github_ref}"', file=sys.stderr)
        sys.exit(1)
    
    return pr_number

def markdown_string():
    return """## Please complete the following checklist:
Thank you, Mirco, for taking the time to review our project. In order to complete the review process, we kindly request your signoff by filling out this checklist. Thanks again! 🙏

### If you did a Code review
- [ ] I've downloaded the code and tested 
- [ ] I don't see bugs in the code
- [ ] The code is justifiably easy to read and understand  
- [ ] The code meets any acceptance criteria agreed to for the work  
- [ ] The code doesn't implement additional and unnecessary functionality  
- [ ] There are no linter errors  
- [ ] The code follows team unit testing standards  
- [ ] The code style and structure follows the project standards as
---
### If you did a Node review
- [ ] I've downloaded the node and tested  
- [ ] I don't see bugs in the functionality of the nodes
- [ ] The nodes have all the inputs and outputs required
- [ ] The nodes are well documented
---
### Document review
- [ ] The documentation clearly describes the implementation
---"""
  
def pull_request_checklist():
    args = read_args()
    if args.token == None or args.token == '':
        print('The action need a GitHub token')
        sys.exit(1)
    
    # Collects GitHub variables.
    repo_name = get_env_var('GITHUB_REPOSITORY')
    github_ref = get_env_var('GITHUB_REF')
    github_event_name = get_env_var('GITHUB_EVENT_NAME')
    
    pr_number = None
    
    # Creates a repository object, using the GitHub token.
    repo = Github(args.token).get_repo(repo_name)
    
    # Gets the pull request number.
    pr_number = get_pr_number(github_ref)
    print(f'Pull request number: {pr_number}')
    
    # Create a pull request object
    pr = repo.get_pull(pr_number)
    pr_reviews = pr.get_reviews()
    
    # Checks if reviews are already open.
    all_match = all(review.state == 'APPROVED' for review in pr_reviews if review.user.login != 'github-actions[bot]')
    if all_match == True:
      pr.create_comment(body= markdown_string())
      
if __name__ == "__main__":
    pull_request_checklist()
