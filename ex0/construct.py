import sys
import os
import site


def is_virtual_env() -> bool:
    if sys.base_prefix == sys.prefix:
        return False
    else:
        return True


def main() -> None:
    if is_virtual_env():
        print("MATRIX STATUS : Welcome to the construct")
        print(f"Current Python: {sys.executable}")
        env_name = os.path.basename(sys.prefix)
        print(f"Virtual Environment: {env_name}")
        print(f"Environment Path : {sys.prefix}")

        print("\nSUCCESS: You're şn an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.\n")

        site_packages = site.getsitepackages()[0]
        print("Package installation path:")
        print(site_packages)

    else:
        print("MATRIX STATUS: You're still plugged in")
        print(f" Current Python: {sys.executable}")
        print("Virtual Environment: Node detected\n")
        print("Warning: You are in the global environment!\n")
        print("The machines can see everything you install.\n")
        print("To enter the construct, run:")
        print("python3 -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\\Scripts\\activate #On Windows")
        print("The run this program again."
              )


if __name__ == "__main__":
    main()
