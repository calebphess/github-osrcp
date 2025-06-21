import os
import csv
import sys

from github import Github
from github import Auth

from dotenv import load_dotenv
load_dotenv()

AUTH_TOKEN = os.getenv('GITHUB_AUTH_TOKEN')

def main(csv_file_path, verbose=False, output_path='./contributors.csv'):
  public_repos = []
  with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      if row:
        public_repos.append(row[0])

  auth = Auth.Token(AUTH_TOKEN)
  github_client = Github(auth=auth)

  users = set()
  user_email = {}
  repo_count = len(public_repos)
  total_merge_count = 0

  for repo_name in public_repos:
    repo = github_client.get_repo(repo_name)
    pulls = repo.get_pulls(state='merged', sort='created', base='main')

    repo_merge_count = 0

    if verbose:
      print(f"----- Merged Pull Requests for {repo.name} -----")
    for pr in pulls:
      if verbose:
        print(f"PR #{pr.number}: {pr.title} by {pr.user.login} (Created at: {pr.created_at})")
      users.add(pr.user.login)
      user_email[pr.user.login] = pr.user.email
      repo_merge_count += 1
    if verbose:
      print(f"Total merged PRs in {repo.name}: {repo_merge_count}")
      print("--------------------------------------------------\n")

    total_merge_count += repo_merge_count

  # Handle output path logic
  if output_path.endswith('/'):
    output_path = os.path.join(output_path, 'contributors.csv')

  with open(output_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['username', 'profile_url', 'email'])
    for user in users:
      email = user_email[user]
      profile_url = f"https://github.com/{user}"
      writer.writerow([user, profile_url, email])
  if verbose:
    print(f"Contributors have been written to {output_path}")

  unique_user_count = len(users)

  print("----- Summary -----")
  print(f"Total repositories processed: {repo_count}")
  print(f"Total merged pull requests: {total_merge_count}")
  print(f"Unique contributors: {unique_user_count}")

  github_client.close()
  
def print_help():
  help_text = """
    github-osrcp.py - Extract unique contributors from merged pull requests across multiple GitHub repositories.

    Usage:
      python github-osrcp.py [<csv_file_path>] [-v] [-o <output_path>]

    Arguments:
      <csv_file_path>    (Optional) Path to a CSV file containing a list of public GitHub repositories (one per line, in 'owner/repo' format).
                         If not provided, the script will look for 'repos.csv' in the current directory.

    Options:
      -v                 Enable verbose output (prints merged PR details for each repository).
      -o <output_path>   Specify output file or directory for the contributors CSV (default: ./contributors.csv).

    Description:
      This script reads a CSV file of GitHub repositories, fetches all merged pull requests on the 'main' branch for each repo,
      collects unique contributor usernames, profile urls and emails, written to a CSV file.
      Requires a GitHub personal access token set as the GITHUB_AUTH_TOKEN environment variable.
    """
  print(help_text)

if __name__ == "__main__":
  verbose = False
  output_path = './contributors.csv'
  args = sys.argv[1:]
  if '--help' in args or '-h' in args:
    print_help()
    sys.exit(0)
  if '-v' in args:
    verbose = True
    args.remove('-v')
  if '-o' in args:
    o_index = args.index('-o')
    try:
      output_path = args[o_index + 1]
      del args[o_index:o_index+2]
    except IndexError:
      print("Error: -o flag requires a path argument.")
      sys.exit(1)
  if len(args) > 1:
    print("Usage: python github-osrcp.py [<csv_file_path>] [-v] [-o <output_path>]")
    sys.exit(1)
  if len(args) == 1:
    csv_file_path = args[0]
  else:
    csv_file_path = 'repos.csv'
    if not os.path.isfile(csv_file_path):
      print("Error: No CSV file provided and 'repos.csv' not found in the current directory.")
      sys.exit(1)
  main(csv_file_path, verbose=verbose, output_path=output_path)
else:
  print("This script is intended to be run as a standalone program.")
  print("Please run it directly to see the output.")
