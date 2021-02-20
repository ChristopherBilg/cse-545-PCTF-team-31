#/bin/sh

echo "Flaskids"
python3 runner.py -m flaskids-exploit
echo "Backup"
python3 runner.py -m backup-exploit
