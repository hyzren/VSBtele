from flask import Flask, render_template
from threading import Thread
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

app = Flask('')

@app.route('/')
def home():
    """Endpoint for uptime monitoring services to ping"""
    return "Bot is alive!"

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "message": "Bot is running"}

def run():
    """Run Flask app on port 5000"""
    # ALWAYS serve the app on port 5000
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    """Creates and starts new thread that runs the flask server."""
    logger.info("Starting keep-alive server...")
    t = Thread(target=run)
    t.start()
    logger.info("Keep-alive server started successfully")

    # Print instructions for setting up UptimeRobot
    # Get the correct Replit URL for this project
    # First try to get from environment variables
    repl_id = os.environ.get('REPL_ID', '')
    repl_slug = os.environ.get('REPL_SLUG', 'telegram-bot-verity')
    repl_owner = os.environ.get('REPL_OWNER', 'Havren')
    
    # Construct the URL based on Replit's URL pattern
    if repl_id:
        # Use the permanent URL format if REPL_ID is available
        repl_url = f"https://{repl_id}.id.repl.co"
    else:
        # Fallback to the standard format
        repl_url = f"https://{repl_slug}.{repl_owner}.repl.co"
    
    print("\n=== HOW TO KEEP YOUR BOT RUNNING 24/7 ===")
    print("1. Go to https://uptimerobot.com and create a free account")
    print("2. Add a new monitor with these settings:")
    print(f"   - URL: {repl_url}")
    print("   - Monitoring Type: HTTP(s)")
    print("   - Monitoring Interval: 5 minutes")
    print("3. Save the monitor and your bot will stay active!")
    print("\nIMPORTANT: To ensure maximum uptime:")
    print("- Use the EXACT URL above for UptimeRobot")
    print("- Deploy your bot using Replit's deployment feature")
    print("- Check dashboard.uptimerobot.com periodically to ensure your monitor is working")
    print("=======================================\n")