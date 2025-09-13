from instabot import Bot
import time

def send_friend_request(username, password, target_user):
    bot = Bot()
    bot.login(username=username, password=password)

    try:
        while True:
            # Send friend request (follow user)
            bot.follow(target_user)
            print(f"Sent follow (friend request) to {target_user}")

            # Instabot does not provide accepted/blocked status directly
            # So we just retry until user manually stops
            print("Waiting before trying again...")
            time.sleep(60)  # avoid rate limits

    except Exception as e:
        print(f"Error: {e}")

    finally:
        bot.logout()

if __name__ == "__main__":
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    target_user = input("Enter the target user ID: ")

    send_friend_request(username, password, target_user)
