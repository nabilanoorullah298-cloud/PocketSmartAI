# PocketSmart AI: Your Smart Budget & Recommendation Assistant

PocketSmart AI is a web app that turns a budget and a list of needs into personalised recommendations using Google's Gemini AI.

![Sample jewelry image used for testing](images/jewelry-sample.png)

## Features
- **Three planners:** Home Interior, Party, and Jewelry
- **AI recommendations:** budget breakdown, product ideas with approximate prices, and money-saving tips
- **Image + text:** upload a reference picture in the Jewelry planner and get similar suggestions
- **User accounts:** register, login and logout with JWT authentication
- **Dashboard and history:** every recommendation is saved and can be viewed again

## Tech stack
- Backend: Python, FastAPI, SQLite
- AI: Google Gemini API (`google-genai`)
- Frontend: HTML, CSS, Jinja2 templates
- Auth: JWT stored in an HTTP-only cookie, passwords hashed with PBKDF2

## Project structure
```
PocketSmartAI/
├── main.py              # FastAPI app and routes setup
├── run.py               # Starts the server
├── config.py            # Settings and environment variables
├── database.py          # SQLite tables and queries
├── security.py          # Password hashing and JWT
├── auth_utils.py        # Current-user helper
├── templating.py        # Jinja2 setup
├── routes/              # auth, dashboard, planner routes
├── services/            # Gemini API calls
├── templates/           # HTML pages
├── static/css/          # Styles
├── images/              # README images
└── requirements.txt
```

## How to run
1. Get a free API key from [Google AI Studio](https://aistudio.google.com).
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the libraries:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project folder:
   ```
   GEMINI_API_KEY=your_key_here
   SECRET_KEY=any_long_random_text
   ```
5. Start the app:
   ```
   python run.py
   ```
6. Open http://127.0.0.1:8000 in your browser, create an account and start planning.

## Notes
- Your `.env` file and the `pocketsmart.db` database are not uploaded to GitHub.
- Prices in the recommendations are AI estimates, not live shop prices.
