import requests, pandas as pd
from config import API_URL

QUERY = """
query GetBids($n:Int!){
  bids(first:$n, orderBy:createdAtTimestamp, orderDirection:desc){
    id
    bidder  { id }
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
    data = r.json()["data"]["bids"]

    rows = []
    for b in data:
        dec = b["currency"]["decimals"]
        rows.append({
            "id":         b["id"],
            "media_id":   b["media"]["id"],
            "bidder":     b["bidder"]["id"],
            "amount_raw": b["amount"],
            "amount_eth": int(b["amount"]) / 10**dec,
            "currency":   b["currency"]["symbol"],
            "timestamp":  pd.to_datetime(int(b["createdAtTimestamp"]), unit="s"),
            "tx_hash":    b["transactionHash"]
        })

    pd.DataFrame(rows).to_csv("zora_bids.csv", index=False)
    print("zora_bids.csv saved:", len(rows), "rows")

if __name__ == "__main__":
    main()
