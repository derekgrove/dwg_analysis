## Github notes:

Should follow these basic principles:

If I'm unsure my local branch is up to date with Github, I should pull:

`git pull origin main`

If I'm working on a new feature, I should make a branch to work on while doing so:

`git checkout -b my-new-feature`

After making changes, i.e. at the end of a work day, I should push my changes:

(while in top-most directory):
```
git add . #adds all changes of files in current directory and subdirectories, i.e. why you should be in top-most directory
git commit -m "Implemented new feature"
git push origin my-new-feature  # Push to GitHub
```

And when I'm finally ready to add my new features to the main branch: 

```
git checkout main
git pull origin main  # Ensure it's up to date
git merge my-new-feature  # Merge the feature branch
git push origin main  # Push the updated main branch
```

I should get in the habit of regulary checking git status for uncommitted changes: 

`git status`