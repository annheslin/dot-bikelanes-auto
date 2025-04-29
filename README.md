# NYC-DOT Bike‐Lane Request Automator

**What**: I created an automatic (well semi-automatic) way to input values for DOT’s Bike-Lane request form so that you can enter more tickets to the DOT without having to fill in the same fields each time. 
The program pauses so that you can manually fill in the cross streets, and fill out the reCAPTCHA. 
You might be wondering, why would I want this? Well, maybe you're like me and want to submit more tickets to the DOT for bike lane requests but find the process of fill out the form manually to be a bit of a pain. 
There are plenty of improvements to make to this program, including dynamic population of the description with dynamic values, dynamically filling out the search based on a csv of files, among others.


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