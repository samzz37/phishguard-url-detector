# PhishGuard — Phishing URL Detector

A student-friendly Flask project with a restrained, professional light interface, based on the supplied presentation, **“Phishing URL Detector: Design Patterns & Architectural Blueprint.”** It demonstrates a layered client-server structure, the Facade Pattern, and the Strategy Pattern.

## What the app does
- Accepts a URL through a responsive browser interface.
- Normalizes the URL and extracts basic structural features.
- Applies three independent heuristic checks: IPv4 host, URL length over 75 characters, and configured deceptive keywords.
- Shows a heuristic score, risk label, and the reasons behind the result.

## Architecture
1. **Presentation layer:** `templates/index.html`, `static/style.css`, `static/app.js`
2. **Control layer:** `app.py` — Flask route, form handling, and page rendering
3. **Business domain layer:** `facade.py` and `strategies.py`
   - `PhishingDetectorFacade` coordinates the analysis.
   - `URLNormalizer` cleans the submitted text.
   - `FeatureExtractor` collects the URL characteristics.
   - Strategy classes apply separate rules.

## Run locally (Windows)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

If PowerShell blocks virtual-environment activation, use Command Prompt:
```bat
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Team division
See `team_packs/` at the project root. Each member has a defined ownership area, deliverables, and integration checklist.

## Important limitation
This is an educational heuristic demonstration, not a production-grade security scanner. It does not open the submitted website, inspect page content, use threat-intelligence feeds, or prove that a URL is safe or malicious. A low score means only that these configured rules did not trigger. Do not enter passwords or other sensitive information.

## Deploy online with Render
1. Push the contents of this `phishing_url_detector` folder to a GitHub repository.
2. Open the Render dashboard and create a new **Web Service** connected to that repository.
3. Use the settings in `render.yaml`, or set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Deploy and open the public `onrender.com` URL Render provides.
