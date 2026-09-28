import sys
import os
import site

def is_virtual_env() -> bool:
    if sys.base_prefix == sys.prefix:
        return(False)
    else:
        return(True)
    

def main() -> None:
    if is_virtual_env():
        print("MATRIX STATUS : Welcome to the construct")
        print(f"{sys.executable}")
    else:
        print("MATRIX STATUS: You're still plugged in")
        print(f"sys.executable")
        print("python3 -m venv matrix_env")
        
if __name__ == "__main__":
    main()
        
        
    