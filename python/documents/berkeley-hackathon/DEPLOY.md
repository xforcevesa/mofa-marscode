# Deployment Guide for MoFA Shop
- based on arch linux

## ENVIRONMENT SETUP

- Clone the Repository

``` shell
git clone https://github.com/chengzi0103/mofa_berkeley_hackathon.git
cd mofa_berkeley_hackathon
git checkout main
```

- Create and Activate the Python Environment 

``` shell
conda create -n shopping-agent python=3.10
conda activate shopping-agent
python -m venv venv
source venv/bin/activate
```

- Install MoFA

And check if the mofa command is available

```
cd python
pip3 install -r requirements.txt
pip3 install -e .
mofa --help
```

- Install Rust and Dora on Arch

``` shell
sudo pacman -S rustup # or any other package manager
rust default stable
cargo install dora-cli --locked
```

## Running the Application 

- Start data-flow

```
cd python/MoFA_marscode/shopping_agents
echo "API_KEY=YOUR_SECRET" > .env.secret
dora up
dora build shopping_dataflow.yml
dora start shopping_dataflow.yml --attach
```

- Lauch the UI

Before running the following commands, make sure there are no important programs running on port 12345.

```
kill -i 12345
cd /mofa_berkeley_hackathon/python/MoFA_marscode/ui
streamlit run socket_client.py
```

