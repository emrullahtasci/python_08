import importlib.metadata
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def check_dependencies() -> bool:
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    packages = ["pandas", "numpy", "matplotlib"]
    all_ready = True

    for pkg in packages:
        try:
            version = importlib.metadata.version(pkg)
            print(f"[OK] {pkg} ({version}) - Ready")
        except importlib.metadata.PackageNotFoundError:
            print(f"[ERROR] {pkg} is missing!")
            all_ready = False

    return all_ready


def analyze_matrix_data() -> None:
    print("\nGenerating Matrix data stream...")

    # 1. NumPy ile 1000 rastgele veri noktası oluşturuyoruz
    np.random.seed(42)
    time_steps = np.arange(1000)
    data_stream = np.sin(time_steps / 50) + np.random.normal(0, 0.2, 1000)

    # 2. Pandas DataFrame oluşturuyoruz
    df = pd.DataFrame({"Time": time_steps, "Signal": data_stream})

    print(f"Data shape: {df.shape}")
    print("First 5 Matrix signal entries:")
    print(df.head())


    plt.figure(figsize=(10, 5))
    plt.plot(df["Time"], df["Signal"], color="green", label="Matrix Stream")
    plt.title("Matrix Data Stream Analysis")
    plt.xlabel("Time Step")
    plt.ylabel("Signal Intensity")
    plt.grid(True)
    plt.legend()

    # Dosya olarak kaydediyoruz
    output_file = "matrix_analysis.png"
    plt.savefig(output_file)
    print(f"\nAnalysis saved to: {output_file}")


def main() -> None:
    if not check_dependencies():
        print("\nMissing dependencies! Please run:")
        print("pip install -r requirements.txt")
        sys.exit(1)

    print("\nAll systems go! Generating visualization...")
    analyze_matrix_data()


if __name__ == "__main__":
    main()