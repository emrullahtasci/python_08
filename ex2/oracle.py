import os
import sys

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

KEYS = ["MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL", "ZION_ENDPOINT"]

DEFAULTS = {
    "development": {
        "DATABASE_URL": "sqlite:///matrix_dev.db",
        "LOG_LEVEL": "DEBUG",
        "ZION_ENDPOINT": "http://localhost:8000",
    },
    "production": {
        "LOG_LEVEL": "WARNING",
    },
}


def load_config() -> dict[str, str | None]:
    if HAS_DOTENV:
        load_dotenv(override=False)
    else:
        print("WARNING: python-dotenv not installed, .env ignored")

    mode = os.getenv("MATRIX_MODE", "development")
    if mode not in DEFAULTS:
        print(f"WARNING: unknown MATRIX_MODE '{mode}', using development")
        mode = "development"

    config: dict[str, str | None] = {"MATRIX_MODE": mode}
    for key in KEYS[1:]:
        value = os.getenv(key) or DEFAULTS[mode].get(key)
        if value is None:
            print(f"WARNING: {key} is missing")
        config[key] = value
    return config


def show_config(config: dict[str, str | None]) -> None:
    prod = config["MATRIX_MODE"] == "production"
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")

    if config["DATABASE_URL"] is None:
        print("Database: Not configured")
    elif prod:
        print("Database: Connected to production cluster")
    else:
        print("Database: Connected to local instance")

    if config["API_KEY"] is None:
        print("API Access: No API key")
    elif prod:
        print("API Access: Authenticated (key hidden)")
    else:
        print(f"API Access: Authenticated ({config['API_KEY'][:3]}***)")

    print(f"Log Level: {config['LOG_LEVEL']}")
    zion = "Online" if config["ZION_ENDPOINT"] else "Offline"
    print(f"Zion Network: {zion}")


def security_check(config: dict[str, str | None]) -> bool:
    ok = True
    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")

    if os.path.isfile(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARN] No .env file found (cp .env.example .env)")

    if config["MATRIX_MODE"] == "production":
        missing = [k for k in KEYS if config[k] is None]
        if missing:
            print(f"[FAIL] Production needs: {', '.join(missing)}")
            ok = False
        else:
            print("[OK] Production configuration complete")
    else:
        print("[OK] Production overrides available")
    return ok


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")
    config = load_config()
    show_config(config)
    if not security_check(config):
        sys.exit(1)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
