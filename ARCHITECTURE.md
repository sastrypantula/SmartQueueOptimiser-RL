# 🏗️ System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│                   http://localhost:3000                      │
│  ┌──────────────┬──────────────┬──────────────────────┐     │
│  │Training Panel│ Sim Panel    │ Queue Visualization  │     │
│  └──────────────┴──────────────┴──────────────────────┘     │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │          Results Panel + Charts                      │    │
│  │      (Recharts: Bar, Line, etc.)                     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           ↕
                    HTTP (Axios)
                           ↕
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                           │
│                 http://localhost:8000                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Endpoints:                                     │   │
│  │  ├── POST /train → Train RL Agent                  │   │
│  │  ├── POST /simulate → Compare Strategies           │   │
│  │  ├── GET /results → Get Results                    │   │
│  │  ├── GET /customers → Queue State                  │   │
│  │  └── GET /health → Health Check                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────┬──────────────┬──────────────────┐    │
│  │  RL Trainer      │ Simulations  │  Queue Manager   │    │
│  │  (stable-bl3)    │  (Strategies)│  (Gym Env)       │    │
│  └──────────────────┴──────────────┴──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend Architecture

### Core Components

#### 1. **Queue Environment** (`queue_env.py`)

A custom Gymnasium environment that simulates a queue system:

```
QueueOptimizationEnv
├── State Representation
│   ├── Queue waiting times
│   ├── Customer priorities
│   ├── Counter availability
│   └── Service time remaining
│
├── Action Space
│   └── Discrete(max_queue_size) → Select customer
│
├── Reward Signal
│   └── -total_waiting_time / 100
│
└── Dynamics
    ├── Customer arrival
    ├── Service completion
    ├── Counter management
    └── Time advancement
```

**Key Methods:**
- `reset()` - Initialize new episode
- `step(action)` - Execute one action, return observation + reward
- `_generate_customers()` - Add new arrivals
- `_serve_customer()` - Process customer at counter
- `_get_observation()` - Convert state to vector

**State Space Details:**
```
Observation Vector (80-dimensional):
├── Positions 0-19: Customer wait times 
├── Positions 20-39: Customer priorities
├── Positions 40-42: Counter busy status
├── Positions 43-45: Service time left per counter
```

#### 2. **RL Trainer** (`train.py`)

Manages PPO/DQN agent training:

```
QueueRLTrainer
├── train()
│   ├── Create environment
│   ├── Initialize model (PPO/DQN)
│   ├── Learn from experience
│   └── Save model
│
├── load_model()
│   └── Restore previously trained model
│
└── evaluate()
    ├── Run episodes
    ├── Collect metrics
    └── Return statistics
```

**Training Process:**
1. Environment generates queue scenarios
2. RL agent observes state
3. Agent selects action (which customer to serve)
4. Environment transitions to new state
5. Reward calculated based on waiting time reduction
6. Agent learns from reward signal
7. Repeat for N timesteps

#### 3. **FastAPI Server** (`main.py`)

REST API for system control:

```
API Routes
├── POST /train
│   └── Triggers RL training
│
├── POST /simulate
│   └── Compares strategies
│
├── GET /results
│   └── Returns latest results
│
├── GET /customers
│   └── Queue state snapshot
│
└── GET /health
    └── Service status
```

**Simulation Strategies:**
- **RL**: Uses trained agent's policy
- **FIFO**: Always serve first customer
- **SJF**: Serve customer with shortest service time

---

## Frontend Architecture

### Component Structure

```
App.js (Main Component)
├── AppBar (Header)
│   └── Title + Navigation
│
├── Container
│   ├── TrainingPanel
│   │   ├── Algorithm Selector
│   │   ├── Hyperparameter Controls
│   │   └── Train Button
│   │
│   ├── SimulationPanel
│   │   ├── Config Controls
│   │   └── Simulate Button
│   │
│   ├── ResultsPanel
│   │   ├── KPI Cards
│   │   ├── Metrics Table
│   │   ├── Bar Chart (Avg Wait Time)
│   │   └── Line Chart (Trends)
│   │
│   └── QueueVisualization
│       ├── Queue Stats
│       ├── Counter Status
│       └── Customer Details Table
│
└── Footer
    └── Credits

```

### Data Flow

```
User Input → Panel Component
    ↓
axios.POST to FastAPI
    ↓
Backend Processing
    ↓
Response with Results
    ↓
Update State (React)
    ↓
Re-render Components
    ↓
Charts Updated
```

### Component Details

**TrainingPanel:**
- Input: Algorithm, timesteps, learning rate
- Output: Training status & model info
- Uses: useState, axios

**SimulationPanel:**
- Input: Counters, steps, episodes
- Output: Triggers simulation
- Uses: useState, axios

**ResultsPanel:**
- Input: Simulation results object
- Output: Charts, metrics, comparisons
- Uses: Recharts components

**QueueVisualization:**
- Input: Auto-fetches from `/customers`
- Output: Live queue display
- Uses: useEffect, intervals

---

## Data Models

### Customer Object
```python
{
    "id": int,                    # Unique customer ID
    "arrival_time": int,          # When customer arrived (step)
    "service_time": int,          # Minutes needed to serve
    "priority": int,              # 1=normal, 2=high, 3=urgent
    "wait_time": int              # Current waiting time
}
```

### Training Config
```python
{
    "algorithm": str,             # "PPO" or "DQN"
    "total_timesteps": int,       # Training duration
    "num_counters": int,          # Service windows
    "learning_rate": float        # Adam learning rate
}
```

### Simulation Results
```python
{
    "rl": {
        "strategy": "RL",
        "avg_wait_time": float,
        "std_wait_time": float,
        "avg_customers_served": int,
        "wait_times": List[float]
    },
    "fifo": {...},
    "sjf": {...},
    "improvements": {
        "rl_vs_fifo": str,        # "34.5%"
        "rl_vs_sjf": str          # "12.3%"
    }
}
```

---

## State Management

### Backend State
- **Global dictionaries**: Store trained models and results
- **Per-request state**: Environment instance for each simulation
- **Stateless design**: Each API call is independent

### Frontend State
- **React hooks**: useState for UI state
- **Axios instances**: Handle API calls
- **No external state management**: Simple for this scale

---

## Training Loop Details

### PPO Agent Training

```
Episode 1                    Episode 2                    Episode N
├── obs, _ = env.reset()     ├── obs, _ = env.reset()    ├── Reset
├── for t in range(steps):   ├── for t in range(steps):  ├── Collect rollouts
│   ├── action = predict()   │   ├── action = predict()  ├── Compute advantages
│   ├── obs, r, d, i = step()│   ├── obs, r, d, i = step()
│   └── reward += r          │   └── reward += r         ├── Update policy
└── Store trajectory         └── Store trajectory         └── Next episode
```

**Key RL Concepts:**

1. **State (Observation)**
   - Queue configuration at current time step
   - Encoded as 80D vector

2. **Action**
   - Integer: which customer (0 to N-1)
   - Discrete choice problem

3. **Reward**
   - Negative cumulative wait time
   - Encourages minimizing total wait
   - Immediate feedback

4. **Policy**
   - Neural network (PPO) or Q-network (DQN)
   - Maps observations to action probabilities

---

## Performance Considerations

### Time Complexity

| Operation | Time | Notes |
|-----------|------|-------|
| Training Step | O(batch_size) | Per gradient update |
| Episode | O(steps) | Per rollout |
| Simulation | O(episodes × steps) | Parallel possible |
| API Response | O(1) | Results lookup |

### Space Complexity

| Component | Memory | Notes |
|-----------|--------|-------|
| Model | ~2-5 MB | Trained PPO |
| Episode | O(steps) | Trajectory buffering |
| Results | ~100 KB | Per simulation |

### Optimization Tips

1. **Batch Processing**: Vectorize environment calls
2. **GPU Training**: Use stable-baselines3 with GPU support
3. **Model Compression**: Prune policy network
4. **Caching**: Store trained models

---

## Deployment Architecture

### Development
```
Local Machine
├── Backend (localhost:8000)
├── Frontend (localhost:3000)
└── Shared filesystem
```

### Production (Optional)
```
Docker Container
├── Backend Service (port 8000)
└── Frontend Service (port 3000)

or

Cloud Platform
├── API Server (AWS Lambda/Heroku)
├── Frontend (Netlify/Vercel)
└── Database (Optional)
```

---

## Error Handling

### Backend
- Input validation (Pydantic models)
- Try-catch blocks for API endpoints
- HTTP status codes (400, 404, 500)

### Frontend
- Error states in components
- User-friendly error messages
- Fallback UI rendering

### Network
- CORS enabled for cross-origin
- Timeout handling
- Retry logic (optional)

---

## Extension Points

### Easy to Add

1. **New Algorithms**: Add to `train.py` (A3C, SAC, etc.)
2. **New Strategies**: Add to `main.py` simulations
3. **New Charts**: Add to `ResultsPanel.js`
4. **Data Persistence**: Add database layer

### Moderate Effort

1. **Multi-agent**: Multiple RL agents learning
2. **Real data**: Connect to actual queue systems
3. **Mobile app**: React Native frontend
4. **Advanced metrics**: More analytics

### Complex

1. **Distributed training**: Ray + RLlib
2. **Production deployment**: Kubernetes
3. **Model serving**: TensorFlow Serving
4. **Real-time updates**: WebSockets

---

**Architecture Decision Record:**
- Chose Gymnasium for standardized RL interface
- Selected FastAPI for async performance
- Used React for interactive UI
- Designed stateless API for scalability
