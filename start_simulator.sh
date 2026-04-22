#!/bin/bash

cd ~/education_complex_systems || exit 1

if [ ! -d ".venv" ]; then
  echo "Ambiente virtual .venv não encontrado."
  exit 1
fi

source .venv/bin/activate

echo "Iniciando Flask..."
nohup python app.py > flask.log 2>&1 &

sleep 3

echo "Iniciando ngrok..."
nohup ngrok http 5000 > ngrok.log 2>&1 &

sleep 5

echo "Processos iniciados."
echo "Veja o link público com:"
echo "curl -s http://127.0.0.1:4040/api/tunnels | python3 -m json.tool"
