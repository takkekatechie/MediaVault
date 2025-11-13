# Removing Large Files From Git History (Safe Guide)

Warning: Rewriting git history is destructive for shared branches. Do this only if you understand the consequences and after coordinating with collaborators.

## Backup (mandatory)

1. Create a mirror clone to preserve the original repository:

```powershell
# run from the parent directory of the repo
git clone --mirror D:\dev\MediaVault D:\dev\MediaVault-backup.git
```

2. Verify the backup exists before proceeding.

## Option A: Use `git-filter-repo` (recommended)

`git-filter-repo` is the modern tool (faster and safer than `filter-branch`). You must have Python and pip available.

### Install

```powershell
pip install git-filter-repo
```

### Remove specific paths (examples)

```powershell
# From inside your repository (not the mirror):
cd D:\dev\MediaVault

# Remove the large model and deployment archive from all commits:
git filter-repo --invert-paths --path models/deepseek-ocr.gguf --path "deployment/MediaVaultScanner_v2.0_20251113.zip" --path "deployment/MediaVaultScanner_v2.0_20251113/MediaVaultScanner.exe"
```

### After rewriting

```powershell
# Force-push rewritten history to remote (you must be prepared to coordinate with collaborators)
git push origin --force --all
git push origin --force --tags
```

## Option B: Use BFG Repo-Cleaner (alternative)

BFG is a simpler wrapper for common cases. It is suitable if you want to remove large files by filename or pattern.

### Steps (BFG)

1. Create a bare clone:

```powershell
git clone --mirror https://github.com/yourusername/MediaVault.git
cd MediaVault.git
```

2. Run BFG to remove files by name or pattern:

```powershell
# example: remove all .gguf files and .zip files
java -jar \path\to\bfg.jar --delete-files "*.gguf" --delete-files "*.zip"
```

3. Cleanup and push:

```powershell
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

## Important Notes & Caveats

- Rewriting history will change commit SHAs. Any collaborators who have cloned or forked this repository will have to rebase or re-clone.
- If the large files have already been pushed to the remote, removing them from local commits alone is not enough — you must force-push the rewritten history.
- Keep a backup (mirror clone) until you are certain the rewrite is successful.
- Notify CI systems and release processes that reference old SHAs.

## Example: Remove one file and preview

If you want to test locally first, clone a fresh copy and run filter-repo there. Do not run these commands on a production branch without confirmation.

---

If you'd like, I can run the `git-filter-repo` command for you (step 3 of the todo list). Reply here to confirm and I'll proceed to run the rewrite and push — but please confirm you accept history rewrite and will coordinate with any collaborators.
