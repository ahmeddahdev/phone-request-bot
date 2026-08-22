import os
import time
import random
from datetime import date
from instagrapi import Client
from instagrapi.exceptions import (
    PleaseWait48Hours,
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    ClientError
)

SESSION_FILE = "session.json"
SESSION_ID = "40472735309:3z8owC39xta2cf:21:AYhL_K-I2FAIx6VXDkdDNlxfae-1KV_AO2B5bLdkeA"
TARGETS = [
    ["gregpizarrojr", "Gregory"],
    ["mansatheinvestor", "Mansa"]
]

START_DATE = date(2026, 5, 13)
today = date.today()
day_count = (today - START_DATE).days + 1

cl = Client()

# Enable automatic internal request delays (2 to 5 seconds between internal API calls)
cl.delay_range = [2, 5]

def get_message(display_name):
    # Combinatorial generator: Intros * Reasons * Closings * Emojis = 2,500+ unique messages!
    intros = [
        f"Day {day_count} of asking {display_name} for an iPhone 13",
        f"Day {day_count} on the quest to get an iPhone 13 from {display_name}",
        f"Checking in for Day {day_count} asking {display_name} for an iPhone 13",
        f"Day {day_count} update for {display_name} (iPhone 13 quest)",
        f"Hey {display_name}! Day {day_count} of the iPhone 13 request journey"
    ]
    
    reasons = [
        "my battery drops 20% every time I open an app 😭",
        "my screen is held together by hope and tape 💔",
        "my phone gets hot enough to warm up coffee 🍳",
        "my camera quality makes HD videos look like 144p 📸",
        "my storage is so full I had to delete my calculator app 💾",
        "my phone takes 5 minutes just to load Instagram DMs ⏳",
        "my speaker sounds like it's underwater 🔊",
        "my phone randomly restarts whenever I receive a call 📞",
        "my touch screen only works on the left side 😂",
        "my flashlight turns on by itself at midnight 🔦",
        "my charger cable has to be bent at a 45 degree angle 🔌",
        "my front camera makes selfies look like Minecraft blocks 🧊"
    ]
    
    closings = [
        "Still on the grind for that iPhone 13!",
        "Keeping the iPhone 13 dream alive!",
        "Sending positive vibes your way!",
        "Hope you're having an awesome week!",
        "Rooting for that iPhone 13 upgrade!",
        "Never giving up on the iPhone 13!"
    ]
    
    emoji_combos = ["💜🚀", "🚀💜", "💜📱🚀", "🚀📱💜", "💜🚀📱", "🚀✨💜", "✨💜🚀"]

    intro = random.choice(intros)
    reason = random.choice(reasons)
    closing = random.choice(closings)
    emoji = random.choice(emoji_combos)
    
    return f"{intro}, {reason} {closing} {emoji}"

def login_with_session():
    print("--- Attempting Login via Session ID ---")
    try:
        # Load existing device settings if present to maintain consistent device identity
        if os.path.exists(SESSION_FILE):
            print(f"Loading persistent device settings from {SESSION_FILE}...")
            cl.load_settings(SESSION_FILE)
        
        # Log in with session ID
        cl.login_by_sessionid(SESSION_ID)
        
        # Save updated settings back to session.json
        cl.dump_settings(SESSION_FILE)
        
        me = cl.account_info().model_dump()
        print(f"Logged in successfully as: {me['username']}")
        return True

    except (PleaseWait48Hours, ChallengeRequired, FeedbackRequired) as e:
        print(f"SECURITY BLOCK DETECTED ({type(e).__name__}): {e}")
        print("Stopping script to protect your account. Please log in manually in browser.")
        return False
    except Exception as e:
        print(f"ERROR during login: {e}")
        return False

def send_dms():
    print(f"\n--- Starting Batch for Day {day_count} ---")
    for username, display_name in TARGETS:
        try:
            target = username.strip()
            
            # Simulated human pre-action pause
            human_pause = random.uniform(3.0, 7.0)
            print(f"Simulating human reading pause ({human_pause:.1f}s)...")
            time.sleep(human_pause)
            
            # Retrieve user info naturally
            user_info = cl.user_info_by_username(target)
            user_id = user_info.pk
            
            # Simulated typing delay before direct_send
            typing_delay = random.uniform(2.5, 6.0)
            print(f"Simulating human typing delay ({typing_delay:.1f}s)...")
            time.sleep(typing_delay)
            
            message = get_message(display_name)
            cl.direct_send(message, [user_id])
            print(f"SUCCESS: Sent to {display_name} (@{target}) -> \"{message}\"")
            
            # Randomized wait interval between targets (18 - 35 seconds)
            batch_delay = random.uniform(18.0, 35.0)
            print(f"Waiting {batch_delay:.1f}s before next action...")
            time.sleep(batch_delay)

        except (PleaseWait48Hours, ChallengeRequired, FeedbackRequired) as e:
            print(f"CRITICAL: Anti-bot trigger hit ({type(e).__name__}): {e}")
            print("Aborting remaining batch to protect account.")
            break
        except Exception as e:
            print(f"Failed to send to {display_name}: {e}")
            
    print(f"Batch completed for Day {day_count}.")

if __name__ == "__main__":
    if login_with_session():
        send_dms()
