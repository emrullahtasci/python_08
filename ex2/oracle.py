import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("ORACLE STATUS: python-dotenv is missing!")
    print("Install it with: pip install -r requirements.txt")
    sys.exit(1)

KEYS = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]
SECRET_KEYS = ["API_KEY", "DATABASE_URL"]
VALID_MODES = ("development", "production")
VALID_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
DEFAULT_LEVEL = {"development": "DEBUG", "production": "WARNING"}


def load_config() -> tuple[dict[str, str | None], set[str]]:
    """Load .env, return config and keys set by the real environment."""
    from_real_env = {key for key in KEYS if key in os.environ}
    # override=False: real environment variables win over .env
    load_dotenv(override=False)
    config = {key: os.getenv(key) or None for key in KEYS}
    return config, from_real_env


def get_mode(config: dict[str, str | None]) -> str:
    mode = config["MATRIX_MODE"]
    if mode is None:
        print("WARNING: MATRIX_MODE is missing, using 'development'")
        return "development"
    if mode not in VALID_MODES:
        print(f"WARNING: invalid MATRIX_MODE '{mode}', using 'development'")
        return "development"
    return mode


def find_missing(config: dict[str, str | None]) -> list[str]:
    return [key for key in KEYS if config[key] is None]


def describe_database(url: str | None) -> str:
    if url is None:
        return "Not configured"
    if "localhost" in url or "127.0.0.1" in url:
        return "Connected to local instance"
    return "Connected to remote server"


def describe_api(key: str | None, mode: str) -> str:
    if key is None:
        return "Not authenticated (no key)"
    if mode == "production":
        return "Authenticated (key hidden)"
    return f"Authenticated (key: {key[:2]}***)"


def describe_zion(url: str | None, mode: str) -> str:
    if url is None:
        return "Offline (no endpoint)"
    if not url.startswith(("http://", "https://")):
        return "Offline (invalid URL)"
    if mode == "production" and not url.startswith("https://"):
        return "Insecure (HTTPS required in production)"
    return "Online"


def check_production_rules(config: dict[str, str | None]) -> list[str]:
    errors = []
    for key in ("DATABASE_URL", "API_KEY", "ZION_ENDPOINT"):
        if config[key] is None:
            errors.append(f"{key} is required in production")
    db = config["DATABASE_URL"]
    if db and ("localhost" in db or "127.0.0.1" in db):
        errors.append("DATABASE_URL must not be local in production")
    if config["LOG_LEVEL"] == "DEBUG":
        errors.append("LOG_LEVEL=DEBUG is not allowed in production")
    return errors


def security_check(
    config: dict[str, str | None], from_real_env: set[str]
) -> None:
    print("\nEnvironment security check:")

    try:
        with open(__file__, encoding="utf-8") as src:
            source = src.read()
    except OSError:
        source = ""
    leaked = [
        key for key in SECRET_KEYS
        if config[key] and config[key] in source
    ]
    if leaked:
        print(f"[FAIL] Hardcoded secrets found: {', '.join(leaked)}")
    else:
        print("[OK] No hardcoded secrets detected")

    try:
        with open(".gitignore", encoding="utf-8") as gi:
            lines = [line.strip() for line in gi]
    except OSError:
        lines = []
    if os.path.isfile(".env") and ".env" in lines:
        print("[OK] .env file properly configured (and git-ignored)")
    elif ".env" not in lines:
        print("[WARN] .env is NOT listed in .gitignore!")
    else:
        print("[WARN] No .env file found (using environment only)")

    if from_real_env:
        names = ", ".join(sorted(from_real_env))
        print(f"[OK] Production overrides active: {names}")
    else:
        print("[OK] Production overrides available")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    config, from_real_env = load_config()
    mode = get_mode(config)

    missing = find_missing(config)
    if missing:
        print(f"WARNING: missing configuration: {', '.join(missing)}")

    level = config["LOG_LEVEL"]
    if level is None:
        level = DEFAULT_LEVEL[mode]
        print(f"WARNING: LOG_LEVEL missing, defaulting to {level}")
    elif level.upper() not in VALID_LEVELS:
        print(f"WARNING: invalid LOG_LEVEL '{level}'")
    config["LOG_LEVEL"] = level

    if mode == "production":
        errors = check_production_rules(config)
        if errors:
            print("\nPRODUCTION WARNINGS:")
            for error in errors:
                print(f"  - {error}")

    print("\nConfiguration loaded:")
    print(f"  Mode: {mode}")
    print(f"  Database: {describe_database(config['DATABASE_URL'])}")
    print(f"  API Access: {describe_api(config['API_KEY'], mode)}")
    print(f"  Log Level: {level}")
    print(f"  Zion Network: {describe_zion(config['ZION_ENDPOINT'], mode)}")

    security_check(config, from_real_env)
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
