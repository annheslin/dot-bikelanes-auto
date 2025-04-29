# NYC-DOT Bike‐Lane Request Automator

**What**: Auto-fills DOT’s Bike-Lane request form for you, one row at a time, and pauses so you can solve the reCAPTCHA.

**Why**: Zero $ cost, runs locally on your laptop.  

---

## Setup

1. **Clone** this repo  
2. `cd dot-bikelanes-auto`  
3. `python3 -m venv venv && source venv/bin/activate`  
4. `pip install -r requirements.txt`  
5. `playwright install`  

## Configure

1. Edit `config.yaml` with your info.  
2. Add all your desired segments (or addresses/intersections) to `locations.csv`.

## Run

```bash
python scripts/submit_request.py