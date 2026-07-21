import sys, os
sys.stdout.reconfigure(encoding="utf-8")

repo_path = r"C:\Users\Administrator\Documents\电化学数据库"

from dulwich import porcelain
from dulwich.repo import Repo

# Init repo
r = Repo.init(repo_path)
print("Repo initialized: " + str(r))

# Add files (recursively - dulwich handles this)
porcelain.add(r, repo_path)
print("Files added")

# Create .gitignore first (done by the previous step)

# Commit
author = b"7vs7wmj2nw-jpg <7vs7wmj2nw-jpg@users.noreply.github.com>"
commit_id = porcelain.commit(
    r,
    "Initial commit - EChemDB electrochemical database",
    author=author,
    committer=author,
)
print("Committed: " + str(commit_id))

# Status
s = porcelain.status(r)
staged = s.staged.get("add", [])
print("Files committed: " + str(len(staged)))
for f in staged[:5]:
    print("  " + str(f))
if len(staged) > 5:
    print("  ... and " + str(len(staged)-5) + " more")
