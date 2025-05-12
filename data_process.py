import pandas as pd
import ast
from pathlib import Path

BASE = Path(".")

def parse_addr(x):
    """
    Accepts:
      • plain address str  "0xABC..."
      • dict‑style str     "{'id': '0xABC...'}"
      • dict object        {"id": "0xABC..."}
    Returns lower‑cased address or None.
    """
    if pd.isna(x):
        return None
    if isinstance(x, dict):          # already a dict
        return x.get("id", "").lower()
    if isinstance(x, str):
        x = x.strip()
        if x.startswith("{") and "id" in x:
            try:
                return ast.literal_eval(x)["id"].lower()
            except Exception:
                return None
        return x.lower()
    return None

def clean_transfers(fp: Path):
    df = pd.read_csv(fp)
    # address fields
    df["from"] = df["from"].apply(parse_addr)
    df["to"]   = df["to"].apply(parse_addr)
    # timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.to_csv(fp, index=False)
    print(f"cleaned transfers → {fp.name} ({len(df)})")

def clean_asks(fp: Path):
    df = pd.read_csv(fp)
    # seller
    df["seller"] = df["seller"].apply(parse_addr)
    # price_eth (calc if missing)
    if "price_eth" not in df.columns or df["price_eth"].isna().all():
        df["price_eth"] = df["price_raw"].astype(float) / 1e18
    # timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.to_csv(fp, index=False)
    print(f"cleaned asks → {fp.name} ({len(df)})")

def clean_bids(fp: Path):
    df = pd.read_csv(fp)
    # bidder
    df["bidder"] = df["bidder"].apply(parse_addr)
    # amount_eth (calc if missing)
    if "amount_eth" not in df.columns or df["amount_eth"].isna().all():
        df["amount_eth"] = df["amount_raw"].astype(float) / 1e18
    # timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.to_csv(fp, index=False)
    print(f"cleaned bids → {fp.name} ({len(df)})")

def validate(fp: Path):
    df = pd.read_csv(fp)
    print("\n— Validation:", fp.name, "—")
    print("rows:", len(df))
    print("nulls per column:\n", df.isna().sum())
    print(df.dtypes)

if __name__ == "__main__":
    clean_transfers(BASE / "zora_transfers.csv")
    clean_asks      (BASE / "zora_asks.csv")
    clean_bids      (BASE / "zora_bids.csv")

    # optional quick validation prints
    for f in ["zora_transfers.csv", "zora_asks.csv", "zora_bids.csv"]:
        validate(BASE / f)
