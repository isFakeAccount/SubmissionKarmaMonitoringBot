import threading
import time
import traceback

import praw
import prawcore

reddit = praw.Reddit("bot")
subreddit = reddit.subreddit("subredditname")  # put subreddit name here

submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)
# These variables are to manage threads as well as sleep timer for exceptions
failed_attempt = 1
bot_running = True
start_time = time.time()

# List which will hold all the submission posted
submission_list = []

# Set the checking interval for upvote using this variable (1 hour is 3600 seconds)
watch_submission_until = 3600
watch_flair = "Shitpost"


# After every 5 minutes the bot will check the submission list
# If a submission is older an hour and still hasn't reached the 20 up votes the bot will delete it
# Note: There might be an error margin of four minutes 59 seconds
def check_upvotes():
    time_now = time.time()
    while bot_running:
        for submission in reversed(submission_list):
            # if submission is older than an hour
            if (time_now - submission.created_utc) >= watch_submission_until:
                # If submission upvotes is less than 20
                if submission.score < 20:
                    submission.mod.remove()
                # remove submission from list as we don't need to watch it anymore
                submission_list.remove(submission)
        time.sleep(300 - ((time.time() - start_time) % 300))


print("Bot is not running {}".format(time.strftime('%I:%M %p %Z')))
# runs the check upvote function in separate thread
check_upvotes_thread = threading.Thread(target=check_upvotes)
check_upvotes_thread.start()
while bot_running:
    try:
        for submission in submission_stream:
            if submission is None:
                break
            # Adds every incoming submission to the submission list where it will stay for an hour
            # After an hour the both will decide whether to remove the submission or leave it as it is
            if submission.link_flair_text == watch_flair:
                submission_list.append(submission)
            failed_attempt = 1
    except KeyboardInterrupt:
        # Stop the bot in elegant way
        bot_running = False
        check_upvotes_thread.join()
        print("Bot has safely Stopped {}".format(time.strftime('%I:%M %p %Z')))
        quit()
    except Exception as exception:
        # prints the traceback
        tb = traceback.format_exc()
        print(tb)
        # In case of server error pause for two minutes
        if isinstance(exception, prawcore.exceptions.ServerError):
            print("Waiting {} minutes".format(2 * failed_attempt))
            # Try again after a pause
            time.sleep(120 * failed_attempt)
            failed_attempt = failed_attempt + 1
        submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)
