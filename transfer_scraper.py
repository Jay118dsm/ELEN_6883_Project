import requests, pandas as pd, time
from datetime import datetime
from config import API_URL

QUERY = """
query GetTransfers($n:Int!,$skip:Int!){
  transfers(first:$n, skip:$skip,
            orderBy:createdAtTimestamp, orderDirection:desc){
    id
    from { id }
    to   { id }
    transactionHash
    createdAtTimestamp
    media { id }
  }
}
"""

def fetch(batch=1000):
    out, skip = [], 0
    while True:
        r = requests.post(API_URL, json={"query": QUERY,
                                         "variables": {"n": batch, "skip": skip}})
        r.raise_for_status()
        page = r.json()["data"]["transfers"]
        if not page:
            break
        out.extend(page)
        print(f"Fetched {len(page)} (total {len(out)})")
        skip += batch
        time.sleep(0.2)
    return out

def main():
    transfers = fetch(1000)
    rows = [{
        "id":         t["id"],
        "media_id":   t["media"]["id"] if t["media"] else None,
        "from":       t["from"]["id"],
        "to":         t["to"]["id"],
        "tx_hash":    t["transactionHash"],
        "timestamp":  pd.to_datetime(int(t["createdAtTimestamp"]), unit="s")
    } for t in transfers]

    pd.DataFrame(rows).to_csv("zora_transfers.csv", index=False)
    print("zora_transfers.csv saved:", len(rows), "rows —", datetime.utcnow(), "UTC")

if __name__ == "__main__":
    main()
