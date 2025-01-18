conda activate mofa

cd shopping_agents/
dora up && dora build shopping_dataflow.yml && dora start shopping_dataflow.yml --detach
setsid nohup hitl-agent &
cd ../ui
streamlit run socket_client.py

