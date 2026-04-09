"""
RL Agent Training Module
Trains PPO agent for queue optimization
"""

from stable_baselines3 import PPO, DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback
import numpy as np
import os
from queue_env import QueueOptimizationEnv


class QueueRLTrainer:
    """Trainer for Q­ueue Optimization RL Agent"""
    
    def __init__(self, model_dir: str = "./models", algorithm: str = "PPO"):
        """
        Initialize the trainer.
        
        Args:
            model_dir: Directory to save trained models
            algorithm: "PPO" or "DQN"
        """
        self.model_dir = model_dir
        self.algorithm = algorithm
        self.model = None
        self.env = None
        
        os.makedirs(model_dir, exist_ok=True)
    
    def train(
        self,
        total_timesteps: int = 100000,
        num_counters: int = 3,
        learning_rate: float = 3e-4,
        save_path: str = None
    ) -> dict:
        """
        Train the RL agent.
        
        Args:
            total_timesteps: Total training timesteps
            num_counters: Number of service counters
            learning_rate: Learning rate for the algorithm
            save_path: Path to save trained model
            
        Returns:
            Training metrics dictionary
        """
        # Create environment
        self.env = QueueOptimizationEnv(
            max_queue_size=20,
            num_counters=num_counters,
            max_steps=500
        )
        
        # Create wrapped environment
        vec_env = DummyVecEnv([lambda: self.env])
        
        # Initialize model
        if self.algorithm == "PPO":
            self.model = PPO(
                "MlpPolicy",
                vec_env,
                learning_rate=learning_rate,
                n_steps=1024,
                batch_size=32,
                n_epochs=4,
                gamma=0.99,
                gae_lambda=0.95,
                clip_range=0.2,
                verbose=1
            )
        elif self.algorithm == "DQN":
            self.model = DQN(
                "MlpPolicy",
                vec_env,
                learning_rate=learning_rate,
                exploration_fraction=0.1,
                exploration_initial_eps=1.0,
                exploration_final_eps=0.05,
                verbose=1,
            )
        
        # Train the model
        print(f"Training {self.algorithm} agent for {total_timesteps} timesteps...")
        self.model.learn(total_timesteps=total_timesteps)
        
        # Save model
        if save_path is None:
            save_path = os.path.join(self.model_dir, f"queue_optimizer_{self.algorithm}")
        
        self.model.save(save_path)
        print(f"Model saved to {save_path}")
        
        return {
            "algorithm": self.algorithm,
            "timesteps": total_timesteps,
            "num_counters": num_counters,
            "model_path": save_path
        }
    
    def load_model(self, model_path: str) -> None:
        """Load a trained model."""
        if self.algorithm == "PPO":
            self.model = PPO.load(model_path)
        elif self.algorithm == "DQN":
            self.model = DQN.load(model_path)
        print(f"Model loaded from {model_path}")
    
    def evaluate(self, num_episodes: int = 10) -> dict:
        """
        Evaluate the trained model.
        
        Args:
            num_episodes: Number of evaluation episodes
            
        Returns:
            Evaluation metrics
        """
        if self.model is None or self.env is None:
            raise ValueError("No model loaded. Train a model first.")
        
        total_rewards = []
        customers_served_list = []
        avg_wait_times = []
        
        for episode in range(num_episodes):
            obs, _ = self.env.reset()
            done = False
            episode_reward = 0
            
            while not done:
                action, _ = self.model.predict(obs, deterministic=True)
                obs, reward, terminated, truncated, info = self.env.step(action)
                episode_reward += reward
                done = terminated or truncated
            
            total_rewards.append(episode_reward)
            customers_served_list.append(info["customers_served"])
            avg_wait_times.append(info["avg_wait_time"])
        
        metrics = {
            "avg_episode_reward": np.mean(total_rewards),
            "std_episode_reward": np.std(total_rewards),
            "avg_customers_served": np.mean(customers_served_list),
            "avg_wait_time": np.mean(avg_wait_times),
        }
        
        return metrics


if __name__ == "__main__":
    # Example training script
    trainer = QueueRLTrainer(algorithm="PPO")
    
    # Train the model
    results = trainer.train(
        total_timesteps=50000,
        num_counters=3,
        learning_rate=3e-4
    )
    print("Training results:", results)
    
    # Evaluate the model
    eval_metrics = trainer.evaluate(num_episodes=5)
    print("Evaluation metrics:", eval_metrics)
