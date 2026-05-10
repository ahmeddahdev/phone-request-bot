import time
import random
from datetime import date
from instagrapi import Client

# 1. Configuration
SESSION_ID = "52735660042:9hwev80HgGe4CI:14:AYi11TOEjpRX_IfJnij0k33tyLGPo-fWR-pQhUHBHg"
TARGETS = [
    ["peller089", "Peller"],
    ["imparkerburton", "Parker Burton"]
]

# 2. Date-Based Counter Logic (Starting May 10, 2026)
START_DATE = date(2026, 5, 10) 
today = date.today()
day_count = (today - START_DATE).days + 1

cl = Client()

def login_with_session():
    print("--- Attempting Login via Session ID ---")
    try:
        cl.login_by_sessionid(SESSION_ID)
        # Verify account
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

            # Small 5-12 second gap to stay stealthy between users
            time.sleep(random.randint(5, 12))

        except Exception as e:
            print(f"Failed to send to {display_name}: {e}")

    print(f"Batch completed for Day {day_count}.")

if __name__ == "__main__":
    if login_with_session():
        send_dms()