# 🔧 Troubleshooting & Testing Guide

## Pre-Launch Checklist

### System Requirements
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 14+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Ports 8000 and 3000 are free
- [ ] Git installed (optional but recommended)

### Installation Verification
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed (`pip list` shows all packages)
- [ ] Frontend dependencies installed (`npm list` shows react, axios, etc.)
- [ ] No error messages during installation

### File Verification
- [ ] All backend files exist (main.py, queue_env.py, train.py, requirements.txt)
- [ ] All frontend files exist (App.js, TrainingPanel.js, etc.)
- [ ] Config files present (config.ini, .gitignore, etc.)
- [ ] Start scripts exist (start_backend.bat, start_frontend.bat)

---

## Common Issues & Solutions

### 1. Python Issues

#### Issue: `python: command not found`
**Symptom**: Error when running python commands
**Solution**:
```bash
# Install Python from https://www.python.org
# When installing, CHECK: "Add Python to PATH"
# Verify:
python --version
# Should show: Python 3.8+
```

#### Issue: `ModuleNotFoundError: No module named 'gymnasium'`
**Symptom**: Import error when starting backend
**Solution**:
```bash
# Ensure venv is activated
cd backend
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall requirements
pip install -r requirements.txt --upgrade

# Verify installation
python -c "import gymnasium; print('OK')"
```

#### Issue: `pip: command not found`
**Symptom**: Can't install packages
**Solution**:
```bash
# Install pip
python -m pip install --upgrade pip

# Verify
pip --version
```

### 2. Backend (FastAPI) Issues

#### Issue: `Port 8000 already in use`
**Symptom**: `Address already in use` error
**Solution**:
```bash
# Option 1: Use different port
python -m uvicorn main:app --port 8001 --reload

# Option 2: Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Unix:
lsof -i :8000
kill -9 <PID>
```

#### Issue: Backend shows import errors
**Symptom**: `ModuleNotFoundError` when starting
**Solution**:
```bash
# Verify virtual environment is active
which python  # Should show path in venv folder

# Reinstall all packages
pip install -r requirements.txt --force-reinstall

# Check for typos in requirements.txt
cat requirements.txt
```

#### Issue: API returns 500 error
**Symptom**: Internal server error when calling endpoints
**Solution**:
```bash
# Check terminal for error messages
# Common causes:
# 1. Pydantic validation error - check JSON format
# 2. RL training timeout - reduce timesteps
# 3. Memory error - close other apps

# Test individually:
curl http://localhost:8000/health
curl http://localhost:8000/customers
```

#### Issue: Model training is extremely slow
**Symptom**: Training takes too long
**Solution**:
```bash
# Reduce training parameters in frontend:
- total_timesteps: 25000 (instead of 50000)
- num_steps: 250 (instead of 500)

# Or edit config.ini:
total_timesteps = 25000
```

### 3. Frontend (React) Issues

#### Issue: `node: command not found`
**Symptom**: Can't run npm commands
**Solution**:
```bash
# Install Node.js from https://nodejs.org
# Verify:
node --version
npm --version
```

#### Issue: `npm install` fails
**Symptom**: Dependencies won't install
**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and lock file
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If still failing, try with verbose:
npm install --verbose
```

#### Issue: `Cannot find module 'axios'`
**Symptom**: React fails to compile
**Solution**:
```bash
cd frontend

# Check if installed
npm list axios

# If missing, install
npm install axios recharts @mui/material @emotion/react @emotion/styled

# Restart dev server
npm start
```

#### Issue: Blank white page or nothing displays
**Symptom**: Browser shows blank page
**Solution**:
```bash
# Check browser console (F12) for errors
# Common causes:
# 1. Backend not running → start backend
# 2. Wrong API URL → check proxy in package.json
# 3. React compilation error → check terminal

# Force refresh
Ctrl+Shift+R  # or Cmd+Shift+R on Mac
```

#### Issue: Charts not displaying
**Symptom**: Results page shows nothing
**Solution**:
```bash
# Ensure Recharts installed
npm list recharts

# If missing:
npm install recharts@2.8.0

# Check browser console for errors
# Verify data is returned from /simulate endpoint
curl http://localhost:8000/results
```

### 4. Communication Issues

#### Issue: `CORS error in browser console`
**Symptom**: `Access to XMLHttpRequest has been blocked by CORS policy`
**Solution**:
```
This means frontend can't reach backend
1. Check backend is running: http://localhost:8000/health
2. Check port is 8000 (not changed)
3. Backend has CORS enabled (should be in main.py)
4. Refresh browser after starting backend
```

#### Issue: `Cannot connect to localhost:8000`
**Symptom**: Connection refused error
**Solution**:
```bash
# Verify backend is running
ps aux | grep uvicorn  # macOS/Linux
tasklist | findstr python  # Windows

# If not running:
cd backend
python -m uvicorn main:app --reload

# Verify it's accessible:
curl http://localhost:8000/health
```

#### Issue: Axios calls timeout
**Symptom**: Requests never return
**Solution**:
```bash
# Backend might be processing
# Training can take 5-15 minutes
# Watch backend terminal for progress

# If completely hung:
# 1. Stop backend (Ctrl+C)
# 2. Check if temporary file is locked
# 3. Restart backend
```

### 5. Environment Variables

#### Issue: API URL is wrong in frontend
**Symptom**: Frontend can't find backend
**Solution**:
```bash
# In frontend/.env (create if not exists)
REACT_APP_API_URL=http://localhost:8000

# Or edit SimulationPanel.js line:
const API_BASE_URL = 'http://localhost:8000';
```

#### Issue: Config.ini not being read
**Symptom**: Configuration isn't applied
**Solution**:
```python
# Config file is referenced but not actively used in current version
# To use config.ini, modify main.py or train.py to read it:

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
```

---

## Performance Testing

### Load Test Results

**Expected on typical machine:**

| Task | Time | Status |
|------|------|--------|
| Health check | < 100ms | ✅ |
| Get queue state | < 100ms | ✅ |
| training (25K steps) | 3-5 min | ✅ |
| Training (50K steps) | 5-10 min | ✅ |
| Simulation (3 strategies, 5 episodes) | 1-2 min | ✅ |
| Frontend load | < 5 sec | ✅ |

### Memory Usage

| Component | RAM | Status |
|-----------|-----|--------|
| Backend (idle) | ~100 MB | ✅ |
| Backend (training) | ~500-800 MB | ✅ |
| Frontend (idle) | ~150 MB | ✅ |
| Total system | ~1-1.5 GB | ✅ |

---

## Testing Scenarios

### Scenario 1: Basic Functionality Test

**Objective**: Verify all components work

```bash
# ✅ Step 1: Backend health
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# ✅ Step 2: Queue snapshot
curl http://localhost:8000/customers
# Expected: queue array with customers

# ✅ Step 3: Frontend loads
Visit http://localhost:3000
# Expected: Dashboard with 4 panels

# ✅ Step 4: API connection test
Open DevTools (F12) → Network tab
Click any button in dashboard
# Expected: Successful API calls (200 status)
```

### Scenario 2: Training Test

**Objective**: Train RL agent successfully

```bash
# ✅ Step 1: Fill training form
- Algorithm: PPO
- Timesteps: 10000 (fast test)
- Counters: 2
- Learning Rate: 0.0003

# ✅ Step 2: Start Training
Click "Start Training"

# ✅ Step 3: Monitor progress
Watch console output
Take 2-3 minutes (with 10K steps)

# ✅ Step 4: Verify completion
Should see: "Training results: {..."
No errors in console
```

### Scenario 3: Simulation Test

**Objective**: Compare strategies

```bash
# Prerequisites: Must train first

# ✅ Step 1: Fill simulation form
- Counters: 2
- Steps: 200 (fast test)
- Episodes: 3

# ✅ Step 2: Run Simulation
Click "Run Simulation"

# ✅ Step 3: View Results
Should see 3 strategy cards:
- RL average wait time
- FIFO average wait time
- SJF average wait time

# ✅ Step 4: Verify metrics
All values > 0
Charts render
Improvements shown (e.g., "32.5%")
```

### Scenario 4: Stress Test

**Objective**: Test with large parameters

```bash
# ✅ Test 1: Large training
- Timesteps: 100000
- Counters: 5
- Should complete in 15-20 min

# ✅ Test 2: Multiple simulations
Run 5 simulations in sequence
Should work without errors

# ✅ Test 3: Dashboard responsiveness
UI should remain responsive
Charts should update smoothly
```

---

## Debugging Tips

### Enable Verbose Logging (Development)

**Backend:**
```python
# In main.py, edit:
app = FastAPI(..., debug=True)

# Or add logging:
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```javascript
// In App.js, add:
axios.interceptors.request.use(req => {
  console.log('Request:', req);
  return req;
});

axios.interceptors.response.use(res => {
  console.log('Response:', res.data);
  return res;
});
```

### Inspect Network Requests

1. Open DevTools (F12)
2. Go to Network tab
3. Perform action (e.g., train)
4. Click request
5. See request/response details

### Check Backend Output

1. Watch terminal where backend is running
2. Look for:
   - INFO: Request logs
   - ERROR: Stack traces
   - Training progress

### Use Postman for API Testing

1. Download Postman
2. Import API collection (see API_DOCS.md)
3. Test each endpoint individually
4. Modify request/response as needed

---

## Recovery Procedures

### If Backend Crashes

```bash
# 1. Hard stop
Ctrl+C in backend terminal

# 2. Check for lock files
rm -f *.lock  # Remove any lock files

# 3. Restart
python -m uvicorn main:app --reload
```

### If Frontend Won't Load

```bash
# 1. Stop React
Ctrl+C in frontend terminal

# 2. Clear cache
rm -rf node_modules/.cache

# 3. Restart
npm start
```

### If Models Are Corrupted

```bash
# 1. Clear models directory
rm -rf backend/models/*

# 2. Retrain from scratch

# Or recover from git:
git checkout backend/models/
```

### Complete Reset

```bash
# Remove everything and start fresh
rm -rf backend/venv backend/models backend/__pycache__
rm -rf frontend/node_modules frontend/build

# Reinstall
cd backend && python -m venv venv
pip install -r requirements.txt

cd ../frontend
npm install

# Restart both
```

---

## Browser Console Errors

### Common Error Messages & Solutions

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to fetch` | Backend not running | Start backend |
| `CORS error` | CORS not enabled | Check main.py |
| `Cannot find module` | Package not installed | `npm install` |
| `Undefined variable` | Wrong component name | Check imports |
| `Port already in use` | Another process on port | Kill process or change port |

---

## Testing Checklist

```
□ Python installed and accessible
□ Node.js installed and accessible
□ Virtual environment created
□ Backend dependencies installed
□ Frontend dependencies installed
□ Backend starts without errors
□ Frontend starts without errors
□ Health endpoint responds
□ Queue endpoint responds
□ Training panel loads
□ Simulation panel loads
□ Results panel loads (after sim)
□ Charts display correctly
□ API calls work (check Network tab)
□ No console errors (F12)
□ Training completes successfully
□ Simulation runs successfully
□ Results show expected data
□ UI is responsive
□ All buttons functional
```

---

## Support & Help

### Getting Help

1. **Check logs**
   - Backend: Terminal output
   - Frontend: Browser console (F12)
   - Both: Check error messages

2. **Read documentation**
   - README.md: General setup
   - API_DOCS.md: API endpoints
   - ARCHITECTURE.md: System design

3. **Test isolation**
   - Test backend independently: `curl` commands
   - Test frontend independently: Remove API calls
   - Test one component at a time

4. **See what's running**
   ```bash
   # Backend process
   ps aux | grep uvicorn
   
   # Frontend process
   ps aux | grep npm
   
   # Open ports
   netstat -tlnp  # Linux
   netstat -abno  # Windows
   """
```

---

## Performance Optimization Tips

### Backend Optimization
- Reduce batch size for faster iterations
- Use GPU (install TensorFlow-GPU)
- Parallelize environments (vectorenv)
- Cache trained models

### Frontend Optimization
- Lazy load components
- Debounce API calls
- Cache results
- Use production build: `npm run build`

---

**Remember: Most issues have simple solutions. Start with checking logs!** 🔍
