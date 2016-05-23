git add .
git commit -m "update content"
git push origin master
call activate ./venv

pelican content -s pelicanconf.py

cd output
git init
git add .
git commit -m "update content"
git push https://%GITHUB_USER%:%GITHUB_PWD%@github.com/%GITHUB_USER%/%GITHUB_USER%.github.io.git master --force
pause