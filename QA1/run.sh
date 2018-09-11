kill -9 `ps -ef | grep client.py|grep -v grep |awk '{print $2}'`
nohup /home/wangy/anaconda3/bin/python3  /home/wangy/wy/QAsystem/QA1/client.py 2>&1 &
