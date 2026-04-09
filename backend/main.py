"""
FastAPI Backend for Smart Queue Optimizer
Serves as API for RL-based queue optimization
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import numpy as np
import json
import os
from queue_env import QueueOptimizationEnv
from train import QueueRLTrainer
import base64
from io import BytesIO


app = FastAPI(title="Smart Queue Optimizer", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
trainers = {}
trained_models = {}
simulation_results = {}


# Pydantic models
class TrainingConfig(BaseModel):
    algorithm: str = "PPO"  # "PPO" or "DQN"
    total_timesteps: int = 50000
    num_counters: int = 3
    learning_rate: float = 3e-4


class SimulationConfig(BaseModel):
    num_counters: int = 3
    num_steps: int = 500
    num_episodes: int = 5


class Customer(BaseModel):
    id: int
    arrival_time: int
    service_time: int
    priority: int
    wait_time: int


class QueueState(BaseModel):
    queue: List[Customer]
    counters_busy: List[bool]
    cumulative_waiting_time: int
    customers_served: int


# Training endpoint
@app.post("/train")
async def train_agent(config: TrainingConfig):
    """
    Train the RL agent for queue optimization.
    
    Args:
        config: Training configuration
        
    Returns:
        Training results and model info
    """
    try:
        trainer = QueueRLTrainer(algorithm=config.algorithm)
        
        results = trainer.train(
            total_timesteps=config.total_timesteps,
            num_counters=config.num_counters,
            learning_rate=config.learning_rate
        )
        
        # Store model
        model_key = f"{config.algorithm}_{config.num_counters}"
        trainers[model_key] = trainer
        
        return {
            "status": "success",
            "message": f"{config.algorithm} agent trained successfully",
            "model_id": model_key,
            "config": config.dict(),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Simulation endpoint
@app.post("/simulate")
async def run_simulation(config: SimulationConfig):
    """
    Run simulation comparing RL vs FIFO vs Shortest Job First.
    
    Args:
        config: Simulation configuration
        
    Returns:
        Comparison results and metrics
    """
    try:
        results = {
            "rl": simulate_with_rl(config),
            "fifo": simulate_with_fifo(config),
            "sjf": simulate_with_sjf(config)
        }
        
        # Calculate improvements
        rl_avg = results["rl"]["avg_wait_time"]
        fifo_avg = results["fifo"]["avg_wait_time"]
        sjf_avg = results["sjf"]["avg_wait_time"]
        
        results["improvements"] = {
            "rl_vs_fifo": f"{((fifo_avg - rl_avg) / fifo_avg * 100):.2f}%",
            "rl_vs_sjf": f"{((sjf_avg - rl_avg) / sjf_avg * 100):.2f}%"
        }
        
        # Store results
        sim_key = f"sim_{len(simulation_results)}"
        simulation_results[sim_key] = results
        
        return {
            "status": "success",
            "simulation_id": sim_key,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Results endpoint
@app.get("/results/{simulation_id}")
async def get_results(simulation_id: str):
    """Get detailed results from a simulation."""
    if simulation_id not in simulation_results:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return simulation_results[simulation_id]


# Latest results endpoint
@app.get("/results")
async def get_latest_results():
    """Get the latest simulation results."""
    if not simulation_results:
        return {"message": "No simulations run yet"}
    
    latest_key = list(simulation_results.keys())[-1]
    return {
        "simulation_id": latest_key,
        "results": simulation_results[latest_key]
    }


# Queue state endpoint
@app.get("/customers")
async def get_queue_state():
    """Get current queue state for visualization."""
    try:
        env = QueueOptimizationEnv(num_counters=3)
        obs, _ = env.reset()
        
        customers_data = [
            {
                "id": c["id"],
                "arrival_time": c["arrival_time"],
                "service_time": c["service_time"],
                "priority": c["priority"],
                "wait_time": c["wait_time"]
            }
            for c in env.queue
        ]
        
        return {
            "queue": customers_data,
            "counters": [
                {
                    "id": i,
                    "busy": c["busy"],
                    "service_time_left": c["service_time_left"]
                }
                for i, c in enumerate(env.counters)
            ],
            "cumulative_waiting_time": env.cumulative_waiting_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Smart Queue Optimizer"}


# ============== Helper Functions ==============

def simulate_with_rl(config: SimulationConfig) -> Dict[str, Any]:
    """Simulate queue using RL agent."""
    env = QueueOptimizationEnv(
        max_queue_size=20,
        num_counters=config.num_counters,
        max_steps=config.num_steps
    )
    
    wait_times = []
    customers_served_list = []
    
    for episode in range(config.num_episodes):
        obs, _ = env.reset()
        done = False
        
        # Use random policy if no trained model
        while not done:
            action = env.action_space.sample()  # Random action
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
        
        wait_times.append(info["avg_wait_time"])
        customers_served_list.append(info["customers_served"])
    
    return {
        "strategy": "RL",
        "avg_wait_time": float(np.mean(wait_times)),
        "std_wait_time": float(np.std(wait_times)),
        "avg_customers_served": float(np.mean(customers_served_list)),
        "wait_times": wait_times
    }


def simulate_with_fifo(config: SimulationConfig) -> Dict[str, Any]:
    """Simulate queue using FIFO (First In First Out) strategy."""
    env = QueueOptimizationEnv(
        max_queue_size=20,
        num_counters=config.num_counters,
        max_steps=config.num_steps
    )
    
    wait_times = []
    customers_served_list = []
    
    for episode in range(config.num_episodes):
        obs, _ = env.reset()
        done = False
        
        # FIFO: always serve first customer in queue
        while not done:
            action = 0 if len(env.queue) > 0 else env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
        
        wait_times.append(info["avg_wait_time"])
        customers_served_list.append(info["customers_served"])
    
    return {
        "strategy": "FIFO",
        "avg_wait_time": float(np.mean(wait_times)),
        "std_wait_time": float(np.std(wait_times)),
        "avg_customers_served": float(np.mean(customers_served_list)),
        "wait_times": wait_times
    }


def simulate_with_sjf(config: SimulationConfig) -> Dict[str, Any]:
    """Simulate queue using Shortest Job First (SJF) strategy."""
    env = QueueOptimizationEnv(
        max_queue_size=20,
        num_counters=config.num_counters,
        max_steps=config.num_steps
    )
    
    wait_times = []
    customers_served_list = []
    
    for episode in range(config.num_episodes):
        obs, _ = env.reset()
        done = False
        
        # SJF: serve customer with shortest service time
        while not done:
            if len(env.queue) > 0:
                action = np.argmin([c["service_time"] for c in env.queue])
            else:
                action = env.action_space.sample()
            
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
        
        wait_times.append(info["avg_wait_time"])
        customers_served_list.append(info["customers_served"])
    
    return {
        "strategy": "SJF",
        "avg_wait_time": float(np.mean(wait_times)),
        "std_wait_time": float(np.std(wait_times)),
        "avg_customers_served": float(np.mean(customers_served_list)),
        "wait_times": wait_times
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
