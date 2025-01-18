kill -15 $(ps -aux | grep hitl | grep mofa | awk '{ print $2 }')
killall dora
kill -15 $(ps -aux | grep streamlit | grep mofa | awk '{ print $2 }')
killall $(which python3)
