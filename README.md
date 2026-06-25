# unitibot
quick calculation solution 

Implementation.

1. Need to create file with bot TOKEN -> BOT_TOKEN.py
<pre>
<code>mkdir data

echo "TOKEN = 'YOUR_BOT_TOKEN_HERE'" > ./data/BOT_TOKEN.py</code>
</pre>
2. Build docker image from Dockerfile:
<pre>
<code>sudo docker build -t calc_bot:latest . </code>
</pre>
3. After build you can try to start it.
<pre>
<code>sudo docker-compose up -d </code>
</pre>
