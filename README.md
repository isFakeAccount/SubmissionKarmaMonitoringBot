# SubmissionKarmaMonitoringBot

## Installing the Requirements

Before running the bots make sure the following requirements are fulfilled.

- Python Version <= 3.8
- Praw Version <= 7.4.0

To install all the python libraries run the following command
```terminal
pip install -r requirements.txt
```

## Configuring the bot

**Configuring the credentials:** 

Put your client ID, secret, reddit account username and password in praw.ini file while looks like this
```editorconfig
[bot]  
client_id=  
client_secret=  
password=  
username=
```
It should look like this. DO NOT PUT VALUES IN DOUBLE/SINGLE QUOTES.
```editorconfig
[bot]
client_id=revokedpDQy3xZ
client_secret=revokedoqsMk5nHCJTHLrwgvHpr
password=invalidht4wd50gk
username=fakebot1
```
See the included template file (`template_praw.ini`), you may edit the file and rename it to `praw.ini` and use it instead.

**Configuring the subreddit:**

Also, in main.py file put the subreddit you want to run this bot on. Put the name without r/
```python
subreddit = reddit.subreddit("subredditname")  # put subreddit name here
```
Put the name without "r/". For example, if someone wants to run the bot on memes. They would write
```python
subreddit = reddit.subreddit("memes")  # put subreddit name here
```