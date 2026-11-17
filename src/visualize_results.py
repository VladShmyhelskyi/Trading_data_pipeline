import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Змінюємо шлях на CSV-файл, який містить дані
INPUT_PATH = os.path.join("data", "processed_market_data.csv")
OUTPUT_DIR = "assets"
OUTPUT_IMAGE = os.path.join(OUTPUT_DIR, "market_analytics_dashboard.png")


def generate_dashboard():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Файл не знайдено: {INPUT_PATH}")

    # 1. Зчитуємо дані з CSV
    df = pd.read_csv(INPUT_PATH)
    df.columns = [str(col).strip() for col in df.columns]

    print(f"📊 Успішно зчитано рядків з CSV: {len(df)}")
    print(f"📋 Колонки: {list(df.columns)}")

    if len(df) == 0:
        print("⚠️ Файл порожній!")
        return

    # 2. Обробка дати та сортування
    date_col = "date" if "date" in df.columns else df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    close_col = "close" if "close" in df.columns else "price"
    ticker = df["symbol"].iloc[0] if "symbol" in df.columns else "EURUSD=X"

    # Розраховуємо прості ковзні середні (SMA) для красивого тренду на графіку
    df["SMA_7"] = df[close_col].rolling(window=7, min_periods=1).mean()
    df["SMA_21"] = df[close_col].rolling(window=21, min_periods=1).mean()

    # 3. Побудова преміального темного дашборду
    plt.style.use("dark_background")
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 6.75), dpi=200,
        gridspec_kw={"height_ratios": [2.6, 1]}, sharex=True
    )
    fig.patch.set_facecolor("#0d1117")

    for ax in (ax1, ax2):
        ax.set_facecolor("#161b22")
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.25, color="#8b949e")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#30363d")
        ax.spines["bottom"].set_color("#30363d")

    # Верхній графік: Ціна закриття та тренди SMA
    ax1.plot(df[date_col], df[close_col], label=f"{ticker} Close Price", color="#58a6ff", linewidth=2)
    ax1.plot(df[date_col], df["SMA_7"], label="SMA 7", color="#3fb950", linewidth=1.3, linestyle="--")
    ax1.plot(df[date_col], df["SMA_21"], label="SMA 21", color="#d29922", linewidth=1.3, linestyle="--")

    ax1.fill_between(df[date_col], df[close_col], df[close_col].min(), color="#58a6ff", alpha=0.06)

    ax1.set_title(
        f"Gold Layer Analytics: {ticker} Price Dynamics & Moving Averages (PySpark → CSV Pipeline)",
        fontsize=12, fontweight="bold", color="#f0f6fc", pad=12, loc="left"
    )
    ax1.set_ylabel("Price (USD)", fontsize=10, color="#c9d1d9")
    ax1.legend(loc="upper left", frameon=True, facecolor="#0d1117", edgecolor="#30363d", fontsize=9)

    # Нижній графік: Обсяг (Volume) або денна зміна
    if "volume" in df.columns:
        ax2.bar(df[date_col], df["volume"], color="#238636", alpha=0.75, width=2)
        ax2.set_ylabel("Volume", fontsize=10, color="#c9d1d9")

    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate(rotation=20)

    # Футер
    fig.text(
        0.012, 0.012,
        f"Source: processed_market_data.csv | Records: {len(df):,} | Stack: Python • PySpark • Pandas • CSV",
        fontsize=8.5, color="#8b949e"
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(OUTPUT_IMAGE, dpi=200)
    print(f"✅ Графік успішно оновлено та збережено у: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    generate_dashboard()