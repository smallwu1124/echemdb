import sys, os
sys.stdout.reconfigure(encoding="utf-8")

repo_path = r"C:\Users\Administrator\Documents\电化学数据库"

# Create .gitignore
gitignore = """__pycache__/
*.pyc
*.pyo
.instance/
*.sqlite3
cloudflared.exe
_turl.txt
_turl2.txt
_fix_*.py
_write_*.py
_git_*.py
*.bat
uploads/
"""

with open(os.path.join(repo_path, ".gitignore"), "w") as f:
    f.write(gitignore)
print("Created .gitignore")

# Init repo and add files
from dulwich import porcelain
from dulwich.repo import Repo

r = Repo.init(repo_path)
print("Initialized repo")

# Add all files (dulwich add works with paths)
porcelain.add(r, repo_path)
print("Added files")

# Commit
author = "7vs7wmj2nw-jpg <7vs7wmj2nw-jpg@users.noreply.github.com>"
porcelain.commit(r, "Initial commit - EChemDB electrochemical database", author=author, committer=author)
print("Committed")

# Verify
status = porcelain.status(r)
print("Status: " + str(len(status.staged.get("add", []))) + " staged, " + str(len(status.untracked)) + " untracked")

print()
print("=== Local repo ready ===")
print("Remote URL: https://github.com/7vs7wmj2nw-jpg/echemdb.git")
