import importlib.metadata
import sys

PACKAGES = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}


def get_version(pkg: str) -> str | None:
    try:
        return importlib.metadata.version(pkg)
    except importlib.metadata.PackageNotFoundError:
        return None


def check_dependencies() -> bool:
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")
    all_ready = True
    for pkg, desc in PACKAGES.items():
        version = get_version(pkg)
        if version is None:
            print(f"[MISSING] {pkg}")
            all_ready = False
        else:
            print(f"[OK] {pkg} ({version}) - {desc}")
    return all_ready


def detect_manager() -> str:
    if sys.prefix == sys.base_prefix:
        return "global Python (no virtual environment)"
    if "pypoetry" in sys.prefix or ".venv" in sys.prefix:
        return "Poetry"
    return "pip (manual venv)"


def compare_managers() -> None:
    print("\npip vs Poetry:")
    print(f"  Running under: {detect_manager()}")
    print(f"  Interpreter  : {sys.executable}")
    print("\n  Installed versions:")
    for pkg in PACKAGES:
        print(f"    {pkg:<12} {get_version(pkg) or 'not installed'}")
    print("\n  pip    : requirements.txt, manual venv, no lock file")
    print("  Poetry : pyproject.toml + poetry.lock, auto venv")
    print("  Run with pip   : python3 loading.py")
    print("  Run with Poetry: poetry run python loading.py")


def analyze_matrix_data() -> None:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    print("\nAnalyzing Matrix data...")
    rng = np.random.default_rng(42)
    signal = rng.normal(0, 1, 1000).cumsum()
    df = pd.DataFrame({"Signal": signal})

    print(f"Processing {len(df)} data points...")
    print(f"Mean: {df['Signal'].mean():.2f}, Std: {df['Signal'].std():.2f}")

    print("Generating visualization...")
    plt.figure(figsize=(10, 5))
    plt.plot(df["Signal"], color="green", label="Matrix Stream")
    plt.title("Matrix Data Stream Analysis")
    plt.xlabel("Time Step")
    plt.ylabel("Signal Intensity")
    plt.grid(True)
    plt.legend()

    output_file = "matrix_analysis.png"
    try:
        plt.savefig(output_file)
    except OSError as e:
        print(f"Could not save file: {e}")
        return
    finally:
        plt.close()

    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:
    if not check_dependencies():
        compare_managers()
        print("\nMissing dependencies! Install them with:")
        print("  pip    : pip install -r requirements.txt")
        print("  Poetry : poetry install")
        sys.exit(1)

    analyze_matrix_data()
    compare_managers()


if __name__ == "__main__":
    main()
