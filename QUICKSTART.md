# 🚀 Quick Start Guide

## Fastest Way to Get Started

### Option 1: One-Command Setup (Windows PowerShell)

```powershell
# Backend
cd .\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload

# In another terminal
cd .\frontend
npm install
npm start
```

### Option 2: Using Batch Scripts

Create `start_backend.bat`:
```batch
cd backend
if not exist venv python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python -m uvicorn main:app --reload
pause
```

Create `start_frontend.bat`:
```batch
cd frontend
npm install
npm start
```

Then just double-click both files.

---

## What to Expect

### First Run (Backend)
- Dependencies install (1-2 min)
- Server starts on http://localhost:8000
- See: "Uvicorn running on http://0.0.0.0:8000"

### First Run (Frontend)
- Dependencies install (2-3 min)
- Webpack builds (1 min)
- Browser opens http://localhost:3000
- See: React dashboard with controls

### First Training
- Takes 5-10 minutes with default settings
- See progress in browser
- Watch terminal for training metrics

### First Simulation
- Takes 1-2 minutes
- Compares RL vs FIFO vs SJF
- Shows charts and metrics

---

## Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'gymnasium'` | `pip install -r requirements.txt` |
| `Port 8000 already in use` | `python -m uvicorn main:app --port 8001` |
| `npm: command not found` | Install Node.js from https://nodejs.org |
| `python: command not found` | Install Python from https://python.org |
| `CORS error in browser` | Backend must be running on http://localhost:8000 |

---

## API Testing with Postman

Import this collection into Postman:

```json
{
  "info": {"name": "Queue Optimizer API"},
  "item": [
    {
      "name": "Health Check",
      "request": {"method": "GET", "url": "http://localhost:8000/health"}
    },
    {
      "name": "Train Agent",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/train",
        "body": {
          "algorithm": "PPO",
          "total_timesteps": 50000,
          "num_counters": 3,
          "learning_rate": 0.0003
        }
      }
    },
    {
      "name": "Run Simulation",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/simulate",
        "body": {
          "num_counters": 3,
          "num_steps": 500,
          "num_episodes": 5
        }
      }
    },
    {
      "name": "Get Results",
      "request": {"method": "GET", "url": "http://localhost:8000/results"}
    },
    {
      "name": "Get Queue State",
      "request": {"method": "GET", "url": "http://localhost:8000/customers"}
    }
  ]
}
```

---

## Dashboard Navigation

```
Landing Page
├── 🤖 RL Agent Training
│   ├── Algorithm Selection
│   ├── Hyperparameter Tuning
│   └── Start Training Button
│
├── 🎮 Run Simulation
│   ├── Queue Configuration
│   ├── Episode Settings
│   └── Execute Simulation
│
├── 📊 Simulation Results
│   ├── Improvement KPIs
│   ├── Strategy Metrics
│   ├── Bar Charts
│   └── Trend Analysis
│
└── 👥 Queue Visualization
    ├── Live Queue Status
    ├── Counter Status
    └── Customer Details
```

---

## Performance Tips

- **Faster Training**: Reduce `total_timesteps` to 25,000
- **Better Results**: Increase `total_timesteps` to 100,000+
- **Quicker Simulations**: Use 2-3 counters instead of 5
- **Development Mode**: VSCode with Python & React extensions

---

## Next Steps

After getting started:

1. ✅ Run default demo (PPO, 3 counters)
2. ✅ Try different algorithms (DQN)
3. ✅ Experiment with parameters
4. ✅ Analyze results
5. ✅ Read detailed README.md
6. ✅ Explore API endpoints
7. ✅ Customize environment
8. ✅ Deploy to production (optional)

---

**Ready? Start backend and frontend, and visit http://localhost:3000** 🎉
