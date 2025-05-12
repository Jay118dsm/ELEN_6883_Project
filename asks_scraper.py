import requests, pandas as pd
from config import API_URL

QUERY = """
query GetAsks($n:Int!){
  asks(first:$n, orderBy:createdAtTimestamp, orderDirection:desc){
    id
    owner   { id }
    amount
    currency{ symbol decimals }
    createdAtTimestamp
    media   { id }
    transactionHash
  }
}
"""

def main():
    r = requests.post(API_URL, json={"query": QUERY, "variables": {"n": 1000}})
    r.raise_for_status()
    data = r.json()["data"]["asks"]

    rows = []
    for a in data:
        dec = a["currency"]["decimals"]
        rows.append({
            "id":         a["id"],
            "media_id":   a["media"]["id"],
            "seller":     a["owner"]["id"],
            "price_raw":  a["amount"],
            "price_eth":  int(a["amount"]) / 10**dec,
            "currency":   a["currency"]["symbol"],
            "timestamp":  pd.to_datetime(int(a["createdAtTimestamp"]), unit="s"),
            "tx_hash":    a["transactionHash"]
        })

    pd.DataFrame(rows).to_csv("zora_asks.csv", index=False)
    print("zora_asks.csv saved:", len(rows), "rows")

if __name__ == "__main__":
    main()
