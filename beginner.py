import time
import schedule
import random
import os
from instagrapi import Client

# Configuration
SESSION_ID = "52735660042:BkMlC3EU623zdD:27:AYicvWkm-YzAsePSDPWH9PhQtmV7KuLEPHuf4az1Pw"

# List of targets: [Instagram Username, Display Name for the message]
TARGETS = [
    ["peller089 ", "Peller"],
    ["imparkerburton ", "Parker Burton"]  # Replace 'jarvis_handle_here' with the actual username
]

cl = Client()


def login_with_session():
    print("--- Attempting Login via Session ID ---")
    try:
        cl.login_by_sessionid(SESSION_ID)
        me = cl.account_info().model_dump()
        print(f"Logged in successfully as: {me['username']}")
        return True
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return False


def send_daily_dm(is_test=False):
    if not is_test:
        # Random wait between 1 and 60 minutes for the whole batch
        wait_seconds = random.randint(60, 3600)
        print(f"\nSchedule triggered! Waiting {wait_seconds // 60} minutes for stealth...")
        time.sleep(wait_seconds)
    else:
        print("\n--- Running Initial Test Send ---")

    # Handle the counter
    if not os.path.exists("counter.txt"):
        with open("counter.txt", "w") as f: f.write("0")

    try:
        with open("counter.txt", "r+") as f:
            content = f.read().strip()
            day = int(content) + 1 if content else 1
            f.seek(0);
            f.write(str(day));
            f.truncate()

        # Loop through both Peller and Jarvis
        for username, display_name in TARGETS:
            try:
                user_id = cl.user_id_from_username(username)

                # Personalized message
                message = f"Day {day} of asking {display_name} for a new phone. 🙏📱"

                cl.direct_send(message, [user_id])
                print(f"SUCCESS: Sent to {display_name} (@{username})")

                # Small 5-10 second gap between sending to the two people
                # This makes the behavior look more 'human'
                time.sleep(random.randint(5, 12))

            except Exception as e:
                print(f"Failed to send to {display_name}: {e}")

        print(f"Batch completed for Day {day}.")

    except Exception as e:
        print(f"Counter/System Error: {e}")


# --- EXECUTION ---
if login_with_session():
    # 1. SEND IMMEDIATELY ON RUN
    send_daily_dm(is_test=True)

    # 2. SCHEDULE FOR THE FUTURE
    # It will wake up at 1:15 PM daily, then wait its random delay
    schedule.every().day.at("13:15").do(send_daily_dm)

    print(f"\nBot is active for {', '.join([t[1] for t in TARGETS])}.")
    while True:
        schedule.run_pending()
        time.sleep(1)