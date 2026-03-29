import os
import argparse

def get_config():
    api_key = os.environ.get("API_KEY")
    db_url  = os.environ.get("DB_URL")

    if not api_key or not db_url:
        raise EnvironmentError("Required secrets not set! Set API_KEY and DB_URL.")
    return {"api_key": api_key, "db_url": db_url}

def main():
    parser = argparse.ArgumentParser(description="Secure Python App")
    parser.add_argument("--check-env", action="store_true", help="Check env vars are set")
    args = parser.parse_args()

    config = get_config()

    if args.check_env:
        print("✅ All required environment variables are present.")
        print(f"   API_KEY  : {'*' * len(config['api_key'])}")
        print(f"   DB_URL   : {'*' * len(config['db_url'])}")

if __name__ == "__main__":
    main()
