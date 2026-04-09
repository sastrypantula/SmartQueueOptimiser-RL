# 📚 API Documentation

## Base URL
```
http://localhost:8000
```

## Interactive API Docs
```
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Purpose:** Verify backend is running

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Smart Queue Optimizer"
}
```

**Status:** ✅ 200 OK

---

### 2. Train RL Agent

**Endpoint:** `POST /train`

**Purpose:** Train a new RL agent

**Request:**
```bash
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "PPO",
    "total_timesteps": 50000,
    "num_counters": 3,
    "learning_rate": 0.0003
  }'
```

**Request Body Schema:**
```python
{
    "algorithm": "PPO" | "DQN",           # RL algorithm
    "total_timesteps": int,                 # Training steps (25000-100000+)
    "num_counters": int,                    # Service counters (1-5)
    "learning_rate": float                  # Learning rate (0.0001-0.001)
}
```

**Response:**
```json
{
  "status": "success",
  "message": "PPO agent trained successfully",
  "model_id": "PPO_3",
  "config": {
    "algorithm": "PPO",
    "total_timesteps": 50000,
    "num_counters": 3,
    "learning_rate": 0.0003
  },
  "results": {
    "algorithm": "PPO",
    "timesteps": 50000,
    "num_counters": 3,
    "model_path": "./models/queue_optimizer_PPO"
  }
}
```

**Status:** ✅ 200 OK | ❌ 500 on error

**Notes:**
- Training takes 5-15 minutes depending on timesteps
- Model saved to `./models/` directory
- Only one training session at a time (blocking)

---

### 3. Run Simulation

**Endpoint:** `POST /simulate`

**Purpose:** Compare RL vs FIFO vs SJF strategies

**Request:**
```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "num_counters": 3,
    "num_steps": 500,
    "num_episodes": 5
  }'
```

**Request Body Schema:**
```python
{
    "num_counters": int,    # Service windows (1-5)
    "num_steps": int,       # Steps per episode (100-1000)
    "num_episodes": int     # Number of episodes (1-20)
}
```

**Response:**
```json
{
  "status": "success",
  "simulation_id": "sim_0",
  "results": {
    "rl": {
      "strategy": "RL",
      "avg_wait_time": 8.234,
      "std_wait_time": 2.156,
      "avg_customers_served": 34.2,
      "wait_times": [8.1, 8.3, 8.2, 8.1, 8.4]
    },
    "fifo": {
      "strategy": "FIFO",
      "avg_wait_time": 12.567,
      "std_wait_time": 3.421,
      "avg_customers_served": 32.4,
      "wait_times": [12.5, 12.6, 12.4, 12.7, 12.5]
    },
    "sjf": {
      "strategy": "SJF",
      "avg_wait_time": 10.789,
      "std_wait_time": 2.876,
      "avg_customers_served": 33.1,
      "wait_times": [10.8, 10.7, 10.9, 10.7, 10.9]
    },
    "improvements": {
      "rl_vs_fifo": "34.54%",
      "rl_vs_sjf": "21.43%"
    }
  }
}
```

**Status:** ✅ 200 OK | ❌ 500 on error

**Notes:**
- Simulates 3 different strategies in parallel
- Each strategy runs for num_episodes
- Results include mean and standard deviation
- Improvements show RL advantage percentage

---

### 4. Get All Results

**Endpoint:** `GET /results`

**Purpose:** Get latest simulation results

**Request:**
```bash
curl http://localhost:8000/results
```

**Response:**
```json
{
  "simulation_id": "sim_0",
  "results": {
    "rl": {...},
    "fifo": {...},
    "sjf": {...},
    "improvements": {...}
  }
}
```

**Status:** ✅ 200 OK

**Notes:**
- Returns the most recent simulation
- If no simulations exist, returns `{"message": "No simulations run yet"}`

---

### 5. Get Specific Results

**Endpoint:** `GET /results/{simulation_id}`

**Purpose:** Retrieve specific simulation results

**Request:**
```bash
curl http://localhost:8000/results/sim_0
```

**Parameters:**
- `simulation_id` (path): ID of simulation (string)

**Response:** Same as above

**Status:** ✅ 200 OK | ❌ 404 if not found

---

### 6. Get Queue State

**Endpoint:** `GET /customers`

**Purpose:** Get current queue state for visualization

**Request:**
```bash
curl http://localhost:8000/customers
```

**Response:**
```json
{
  "queue": [
    {
      "id": 0,
      "arrival_time": 5,
      "service_time": 3,
      "priority": 1,
      "wait_time": 12
    },
    {
      "id": 1,
      "arrival_time": 8,
      "service_time": 2,
      "priority": 3,
      "wait_time": 9
    }
  ],
  "counters": [
    {
      "id": 0,
      "busy": true,
      "service_time_left": 2
    },
    {
      "id": 1,
      "busy": false,
      "service_time_left": 0
    },
    {
      "id": 2,
      "busy": true,
      "service_time_left": 5
    }
  ],
  "cumulative_waiting_time": 21
}
```

**Status:** ✅ 200 OK | ❌ 500 on error

**Notes:**
- Returns snapshot of current queue state
- Call frequently to monitor live status
- Priority: 1=Normal, 2=High, 3=Urgent

---

## Response Codes

| Code | Meaning | Scenario |
|------|---------|----------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid parameters or format |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Backend processing error |

---

## Error Responses

### Error Format
```json
{
  "detail": "Error message explaining what went wrong"
}
```

### Example Error
```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{"num_counters": "invalid"}'
```

**Response:**
```json
{
  "detail": "Input should be a valid integer [type=int_type]..."
}
```

---

## Request/Response Times

| Endpoint | Time | Notes |
|----------|------|-------|
| `/health` | < 10ms | Instant |
| `/train` | 5-15 min | Depends on timesteps |
| `/simulate` | 1-3 min | Depends on episodes/steps |
| `/results` | < 50ms | Just lookup |
| `/customers` | < 50ms | Just lookup |

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Check health
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Train agent
train_config = {
    "algorithm": "PPO",
    "total_timesteps": 50000,
    "num_counters": 3,
    "learning_rate": 0.0003
}
response = requests.post(f"{BASE_URL}/train", json=train_config)
print(response.json())

# Run simulation
sim_config = {
    "num_counters": 3,
    "num_steps": 500,
    "num_episodes": 5
}
response = requests.post(f"{BASE_URL}/simulate", json=sim_config)
results = response.json()
print(results)

# Get results
response = requests.get(f"{BASE_URL}/results")
print(response.json())
```

---

## JavaScript/Axios Example

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Health check
const checkHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    console.log('Backend healthy:', response.data);
  } catch (error) {
    console.error('Backend error:', error);
  }
};

// Train agent
const trainAgent = async () => {
  try {
    const config = {
      algorithm: 'PPO',
      total_timesteps: 50000,
      num_counters: 3,
      learning_rate: 0.0003
    };
    const response = await axios.post(`${API_BASE_URL}/train`, config);
    console.log('Training started:', response.data);
  } catch (error) {
    console.error('Training error:', error.response.data);
  }
};

// Run simulation
const runSimulation = async () => {
  try {
    const config = {
      num_counters: 3,
      num_steps: 500,
      num_episodes: 5
    };
    const response = await axios.post(`${API_BASE_URL}/simulate`, config);
    console.log('Simulation results:', response.data.results);
  } catch (error) {
    console.error('Simulation error:', error.response.data);
  }
};

// Get results
const getResults = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/results`);
    console.log('Latest results:', response.data);
  } catch (error) {
    console.error('Error fetching results:', error);
  }
};
```

---

## CURL Batch Testing

Run all endpoints:
```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "1. Health Check"
curl $BASE_URL/health

echo -e "\n\n2. Train Agent"
curl -X POST $BASE_URL/train \
  -H "Content-Type: application/json" \
  -d '{"algorithm":"PPO","total_timesteps":50000,"num_counters":3,"learning_rate":0.0003}'

echo -e "\n\n3. Run Simulation"
curl -X POST $BASE_URL/simulate \
  -H "Content-Type: application/json" \
  -d '{"num_counters":3,"num_steps":500,"num_episodes":5}'

echo -e "\n\n4. Get Results"
curl $BASE_URL/results

echo -e "\n\n5. Get Queue State"
curl $BASE_URL/customers
```

---

## Postman Collection

Import into Postman:
```json
{
  "info": {
    "name": "Smart Queue Optimizer API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {"method": "GET", "url": "{{base_url}}/health"}
    },
    {
      "name": "Train Agent",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/train",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"algorithm\": \"PPO\",\n  \"total_timesteps\": 50000,\n  \"num_counters\": 3,\n  \"learning_rate\": 0.0003\n}"
        }
      }
    },
    {
      "name": "Run Simulation",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/simulate",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"num_counters\": 3,\n  \"num_steps\": 500,\n  \"num_episodes\": 5\n}"
        }
      }
    },
    {
      "name": "Get Results",
      "request": {"method": "GET", "url": "{{base_url}}/results"}
    },
    {
      "name": "Get Queue State",
      "request": {"method": "GET", "url": "{{base_url}}/customers"}
    }
  ]
}
```

Set `base_url` variable in Postman to `http://localhost:8000`

---

## Rate Limiting

Currently not implemented. In production, consider:
- Max 1 training job at a time
- Max 10 simulations per minute
- Queue API calls with token bucket

---

## Versioning

Current API Version: **1.0.0**

Future versions may include:
- `/v2/train`
- Authentication
- Pagination for results
