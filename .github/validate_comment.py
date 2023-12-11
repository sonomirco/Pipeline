import sys
import re
import argparse

# Constants--
CODE_REVIEW_SECTION = "If you did a Code review"
NODE_REVIEW_SECTION = "If you did a Node review"
DOCUMENT_REVIEW_SECTION = "Document review"
UNCHECKED_BOX = '- [ ]'
CHECKED_BOX = '- [x]'
EXCLUDED_CHECKBOX = "The code follows team unit testing standards"

def read_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review the checklist has be compleated", formatter_class=argparse.RawTextHelpFormatter)
    # We will parse the list as a string.
    parser.add_argument("--body", type=str, help="The checklist body")
    args = parser.parse_args()
    return args

def extract_checkboxes_from_section(comment, section):
    section_pattern = f"### {section}(.*?)---"
    section_content = re.search(section_pattern, comment, re.DOTALL)
    
    if not section_content:
        return []

    checkboxes = [' '.join(item) for item in re.findall(r'(- \[[ xX]\]) (.*?)(\n|")', section_content.group())]

    if section == CODE_REVIEW_SECTION:
        checkboxes = [c for c in checkboxes if EXCLUDED_CHECKBOX not in c]

    return checkboxes

def are_all_checked(checks):
    return all(CHECKED_BOX in check for check in checks)

def are_all_unchecked(checks):
    return all(UNCHECKED_BOX in check for check in checks)

def validate_checklist():
    args = read_args()
    if args.body == None or args.body == '':
        print('The action need the checklist body')
        sys.exit(1)

    code_review_checks = extract_checkboxes_from_section(args.body, CODE_REVIEW_SECTION)
    node_review_checks = extract_checkboxes_from_section(args.body, NODE_REVIEW_SECTION)
    document_review_checks = extract_checkboxes_from_section(args.body, DOCUMENT_REVIEW_SECTION)

    if not are_all_checked(document_review_checks):
        return False

    # Validate Code review
    is_code_review_valid = are_all_checked(code_review_checks) or are_all_unchecked(code_review_checks)

    # Validate Node review
    is_node_review_valid = are_all_checked(node_review_checks) or are_all_unchecked(node_review_checks)

    # If either code review or node review is invalid, return False
    if not (is_code_review_valid and is_node_review_valid):
        sys.exit(1)

# By default, a script that completes without any errors will exit with a status of 0, which indicates success. 

if __name__ == "__main__":
    validate_checklist()
