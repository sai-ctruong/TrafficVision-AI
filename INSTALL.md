# TrafficAI Pro Installation

## 1. Create or activate a Python environment

Python 3.9 or newer is supported.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Add the YOLO model

The app uses `best_oto.pt` from the project root by default. You can also choose another `.pt` file from the Settings page.

## 4. Run

```powershell
python main.py
```

The new modular application lives in `TrafficAIPro/`.
