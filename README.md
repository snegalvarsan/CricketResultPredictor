## Cricket Match Predictor – ML Project Summary

This project is a web app that predicts the winner of a cricket match using historical data from [Cricsheet.org](https://cricsheet.org). It uses a trained ML model and has a nice user interface built with Streamlit.

---

### What it does:

* Predicts which team will win based on:

  * Team names
  * Toss winner & decision
  * Venue
* Shows win probability as a percentage
* Updates data daily using `cron`
* Runs in a Docker container and is accessible via your VM's public IP

---

### How to run:

1. Clone the project:

   ```bash
   git clone https://github.com/snegalvarsan/CricketResultPredictor.git
   cd CricketResultPredictor
   ```

2. Run the setup:

   ```bash
   sh ./setup.sh
   ```

3. Visit your app:
   Please wait for 5-10 minutes for the ML model to be deployed and implemented.
   ```
   http://<your-vm-public-ip>
   ```
---

### 🧠 Data & Model:

* Uses IPL match data from Cricsheet
* Trained on `team1`, `team2`, `venue`, `toss_winner`, and `toss_decision`
* Uses RandomForestClassifier
* Gives predictions + win % for both teams

 Cricsheet data is open and free for non-commercial and research purposes.
