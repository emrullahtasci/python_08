import sys
import os
import site


def is_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def main() -> None:
    if is_virtual_env():
        print("MATRIX STATUS: Welcome to the construct")
        print(f"Current Python: {sys.executable}")
        env_name = os.path.basename(sys.prefix)
        print(f"Virtual Environment: {env_name}")
        print(f"Environment Path: {sys.prefix}")

        print("\nSUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.\n")

        site_packages = site.getsitepackages()[0]
        print("Package installation path:")
        print(site_packages)
        print(f"\nGlobal Python: {sys.base_prefix}")

    else:
        print("MATRIX STATUS: You're still plugged in")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected\n")
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")

        print("Global package location:")
        print(site.getsitepackages()[0])
        print()

        print("To enter the construct, run:")
        print("python3 -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\\Scripts\\activate # On Windows")
        print("Then run this program again.")


if __name__ == "__main__":
    main()
