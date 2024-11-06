#bin/bash
@echo off

if [ -f install.lock ]; then
    echo "Install lock file found, skipping installation"
else
    sed -i "s|[此处填写你的API-KEY]|${OPENAI_KEY}|g" /app/config.json
    sed -i "s|[此处填写你的API地址]|${OPENAI_API}|g" /app/config.json
    sed -i "s|[此处填写AI模型名]|${OPENAI_MODEL}|g" /app/config.json

    echo "Replacing API key with $OPENAI_KEY"
    echo "Replacing API address with $OPENAI_API"
    echo "Replacing AI model with $OPENAI_MODEL"

    pip install -r requirements.txt
    touch install.lock

    echo "Installation complete"
fi

python main.py