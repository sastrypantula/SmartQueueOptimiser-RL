"""
Queue Optimization Environment for Reinforcement Learning
Custom Gymnasium environment for queue simulation
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Tuple, Dict, Any


class QueueOptimizationEnv(gym.Env):
    """
    Custom environment for queue optimization using RL.
    
    State: Current queue snapshot (waiting times, priorities, counter availability)
    Action: Select next customer to serve
    Reward: Negative total waiting time (minimize waiting)
    """
    
    metadata = {"render_modes": ["human"]}
    
    def __init__(self, max_queue_size=20, num_counters=3, max_steps=1000):
        """
        Initialize the queue environment.
        
        Args:
            max_queue_size: Maximum customers in queue at once
            num_counters: Number of service counters
            max_steps: Maximum steps per episode
        """
        super().__init__()
        
        self.max_queue_size = max_queue_size
        self.num_counters = num_counters
        self.max_steps = max_steps
        self.current_step = 0
        
        # State space: [waiting_times(max_queue_size), priorities(max_queue_size), 
        #               counter_busy(num_counters), service_times_left(num_counters)]
        state_dim = max_queue_size * 2 + num_counters * 2
        self.observation_space = spaces.Box(
            low=0, high=1000, shape=(state_dim,), dtype=np.float32
        )
        
        # Action space: select which customer to serve (0 to max_queue_size-1)
        self.action_space = spaces.Discrete(max_queue_size)
        
        # Initialize queue
        self.queue = []  # List of {id, arrival_time, service_time, priority, wait_time}
        self.counters = [{"busy": False, "service_time_left": 0} for _ in range(num_counters)]
        self.cumulative_waiting_time = 0
        self.customers_served = 0
        self.total_wait_time = 0
        
    def reset(self, *, seed=None, options=None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset environment to initial state."""
        super().reset(seed=seed)
        
        if seed is not None:
            np.random.seed(seed)
        
        self.queue = []
        self.counters = [
            {"busy": False, "service_time_left": 0} 
            for _ in range(self.num_counters)
        ]
        self.cumulative_waiting_time = 0
        self.customers_served = 0
        self.total_wait_time = 0
        self.current_step = 0
        
        # Generate initial customers
        self._generate_customers(num_customers=5)
        
        return self._get_observation(), {}
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Execute one step of the environment.
        
        Args:
            action: Index of customer to serve next
            
        Returns:
            observation, reward, terminated, truncated, info
        """
        self.current_step += 1
        truncated = False
        terminated = False
        
        # Validate action
        if len(self.queue) > 0 and 0 <= action < len(self.queue):
            # Serve the selected customer
            self._serve_customer(action)
        else:
            # If no valid customer, advance time
            self._advance_time()
        
        # Update queue wait times
        for customer in self.queue:
            customer["wait_time"] += 1
        
        self.cumulative_waiting_time = sum(c["wait_time"] for c in self.queue)
        
        # Generate new customers occasionally
        if np.random.random() < 0.3:  # 30% chance per step
            self._generate_customers(num_customers=1)
        
        # Calculate reward (negative waiting time)
        reward = -self.cumulative_waiting_time / 100.0
        
        # Episode ends if max steps reached or queue stabilized
        if self.current_step >= self.max_steps:
            terminated = True
        
        observation = self._get_observation()
        info = {
            "queue_size": len(self.queue),
            "customers_served": self.customers_served,
            "avg_wait_time": self.total_wait_time / max(1, self.customers_served)
        }
        
        return observation, reward, terminated, truncated, info
    
    def _serve_customer(self, customer_idx: int) -> None:
        """Serve a customer from the queue."""
        if customer_idx >= len(self.queue):
            return
        
        # Find available counter
        available_counter = None
        for i, counter in enumerate(self.counters):
            if not counter["busy"]:
                available_counter = i
                break
        
        if available_counter is not None:
            customer = self.queue.pop(customer_idx)
            service_time = customer["service_time"]
            
            # Assign to counter
            self.counters[available_counter]["busy"] = True
            self.counters[available_counter]["service_time_left"] = service_time
            
            # Track metrics
            self.customers_served += 1
            wait_time = customer["wait_time"]
            self.total_wait_time += wait_time
        else:
            self._advance_time()
    
    def _advance_time(self) -> None:
        """Advance time on all busy counters."""
        for counter in self.counters:
            if counter["busy"] and counter["service_time_left"] > 0:
                counter["service_time_left"] -= 1
                if counter["service_time_left"] == 0:
                    counter["busy"] = False
    
    def _generate_customers(self, num_customers: int = 1) -> None:
        """Generate new customers arriving in the queue."""
        for _ in range(num_customers):
            if len(self.queue) < self.max_queue_size:
                customer = {
                    "id": len(self.queue),
                    "arrival_time": self.current_step,
                    "service_time": np.random.randint(2, 8),  # 2-7 minutes
                    "priority": np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1]),  # 1=normal, 3=urgent
                    "wait_time": 0
                }
                self.queue.append(customer)
    
    def _get_observation(self) -> np.ndarray:
        """Convert current state to observation vector."""
        obs = np.zeros(self.max_queue_size * 2 + self.num_counters * 2, dtype=np.float32)
        
        # Queue waiting times and priorities
        for i, customer in enumerate(self.queue[:self.max_queue_size]):
            obs[i] = customer["wait_time"]
            obs[self.max_queue_size + i] = customer["priority"]
        
        # Counter availability and service time left
        for i, counter in enumerate(self.counters):
            obs[self.max_queue_size * 2 + i] = 1.0 if counter["busy"] else 0.0
            obs[self.max_queue_size * 2 + self.num_counters + i] = counter["service_time_left"]
        
        return obs
    
    def render(self, mode: str = "human") -> None:
        """Render the queue state."""
        print(f"\n--- Step {self.current_step} ---")
        print(f"Queue size: {len(self.queue)}")
        print(f"Waiting time (cumulative): {self.cumulative_waiting_time}")
        print(f"Customers served: {self.customers_served}")
        print("Queue:", [c["id"] for c in self.queue[:5]])
