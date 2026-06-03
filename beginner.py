import time
import random
from datetime import date
from instagrapi import Client

SESSION_ID = "52735660042:LgCIh4N4nUfX8h:18:AYiPkKtV7mg3rsJd-7e4M6a5pPs7MnC4csN6P1iR9A"
TARGETS = [
    ["peller089", "Peller"]
]

START_DATE = date(2026, 5, 13)
today = date.today()
day_count = (today - START_DATE).days + 1

cl = Client()

def login_with_session():
    print("--- Attempting Login via Session ID ---")
    try:
        cl.login_by_sessionid(SESSION_ID)
        me = cl.account_info().model_dump()
        print(f"Logged in successfully as: {me['username']}")
        return True
    except Exception as e:
        print(f"CRITICAL ERROR during login: {e}")
        return False

def send_dms():
    print(f"\n--- Starting Batch for Day {day_count} ---")
    for username, display_name in TARGETS:
        try:
            target = username.strip()
            user_id = cl.user_id_from_username(target)
            message = f"Day {day_count} of asking {display_name} for a new phone. 🙏📱"
            cl.direct_send(message, [user_id])
            print(f"SUCCESS: Sent to {display_name} (@{target})")
            time.sleep(random.randint(5, 12))
        except Exception as e:
            print(f"Failed to send to {display_name}: {e}")
    print(f"Batch completed for Day {day_count}.")

if __name__ == "__main__":
    if login_with_session():
        send_dms()
