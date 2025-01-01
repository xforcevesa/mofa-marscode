#!/bin/bash
# test

echo "loading..."
git clone https://github.com/xforcevesa/mofa-marscode
cd mofa-marscode
git checkout main
conda create -n shopping-agent python=3.10 -y
conda activate shopping-agent
python -m venv venv
source venv/bin/activate

echo "Installing python dependencies..."
cd python
pip3 install -r requirements.txt
pip3 install -e .
mofa --help
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
cargo install dora-cli --locked
echo "Setting up environment variables..."
cd ../python/MoFA_marscode/shopping_agents
echo "API_KEY=YOUR_SECRET" > .env.secret

echo "dataflow booting"
dora up
dora build shopping_dataflow.yml
dora start shopping_dataflow.yml --attach
cd ../../../python/MoFA_marscode/ui
streamlit run socket_client.py &

echo "Checking for port conflicts..."
PORT=12345
if lsof -i :$PORT > /dev/null; then
    echo "Port $PORT is occupied. Terminating the process..."
    PID=$(lsof -t -i :$PORT)
    kill -9 $PID
    echo "Process terminated. Restarting Streamlit..."
    streamlit run socket_client.py &
else
    echo "Port $PORT is free."
fi

echo "Deployment completed successfully!"
