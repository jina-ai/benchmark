git config user.name "Jina Dev Bot"
git config user.email bot@jina.ai
git add -A
git commit -m "feat: added Jina ${git_tag} benchmark outputs"

# push changes to upstream
i=0
while ! git push && [[ $i -lt 2 ]]
do
  ((i++))
  git fetch
  git merge origin/main
  sleep 3
done
