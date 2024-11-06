#bin/bash
set -x
cd /app || exit

if [ -f install.lock ]; then
    echo "Install lock file found, skipping installation"
else
    pip install -r requirements.txt
    touch install.lock

    echo "Installation complete"
fi

python main.py