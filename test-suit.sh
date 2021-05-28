# !/bin/bash
set -eu


project_dir="$HOME/Desktop/python/Data-engineering/fifth-week"

if [[ $(pwd) != ${project_dir}]];
then
echo - e "Not in project directory. Changing directory to ${project_dir}\n"
cd ${project_dir}
fi
if pytest-3 pytest tests/tests.py -v;
then
    git commit -am "${1}"
    git push origin main
fi