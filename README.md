# Zora NFT Data Pipeline

Scripts that reproduce Phase 2 of our ELEN 6883 final project.

## Files
| file | purpose |
|------|---------|
| `config.py`           | shared GraphQL endpoint |
| `transfer_scraper.py` | grabs latest transfers → `zora_transfers.csv` |
| `asks_scraper.py`     | grabs latest 1 000 asks  → `zora_asks.csv` |
| `bids_scraper.py`     | grabs latest 1 000 bids  → `zora_bids.csv` |
| `data_process.py`     | optional merge into `zora_events_combined.csv` |
| `requirements.txt`    | dependencies |

## Quick start

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python transfer_scraper.py
python asks_scraper.py
python bids_scraper.py

# optional consolidation
python process_data.py
