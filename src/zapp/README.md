```sh
virtualenv -p python3 zappvenv
source zappvenv/bin/activate
pip install -r zapp.requirements.txt
zappa deploy dev
```