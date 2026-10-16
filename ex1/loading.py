import importlib.metadata
import sys


def check_dependencies() -> bool:
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    packages = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "matplotlib": "Visualization ready",
    }
    all_ready = True

    for pkg, desc in packages.items():
        try:
            version = importlib.metadata.version(pkg)
            print(f"[OK] {pkg} ({version}) - {desc}")
        except importlib.metadata.PackageNotFoundError:
            print(f"[MISSING] {pkg}")
            all_ready = False

    return all_ready


def compare_managers() -> None:
    print("\npip vs Poetry:")
    print("  pip    : requirements.txt, manual venv, no lock file")
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
        print("\nMissing dependencies! Install them with:")
        print("  pip    : pip install -r requirements.txt")
        print("  Poetry : poetry install")
        sys.exit(1)

    analyze_matrix_data()
    compare_managers()


if __name__ == "__main__":
    main()
