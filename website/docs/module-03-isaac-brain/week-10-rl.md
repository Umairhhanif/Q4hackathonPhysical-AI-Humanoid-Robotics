---
title: "Week 10: Reinforcement Learning"
sidebar_position: 3
---

# Week 10: Reinforcement Learning for Robot Control

## Training Robots to Learn Like Humans

This week introduces **Reinforcement Learning (RL)**, the paradigm shift enabling robots to learn complex skills through trial and error. Instead of hard-coding behaviors, you'll create environments where agents learn to walk, grasp, and navigate by maximizing rewards. We'll leverage Isaac Gym for massively parallel training, compressing years of robotic experience into minutes of simulation time.

## RL Fundamentals

### The RL Loop
The interaction between an **Agent** and an **Environment**:
1.  **State (`$s_t$`)**: The agent observes the current situation.
2.  **Action (`$a_t$`)**: The agent takes an action based on its policy `$\pi$`.
3.  **Reward (`$r_t$`)**: The environment provides feedback on the action's quality.
4.  **Next State (`$s_{t+1}$`)**: The environment transitions to a new state.

**Goal**: Maximize cumulative reward `$R = \sum \gamma^t r_t$` over time.

### Key Components
- **Policy (`$\pi$`)**: The brain. Maps states to actions (`$a = \pi(s)$`).
- **Value Function (`$V(s)$`)**: Prediction of future rewards from state `$s$`.
- **Model**: Representation of how the environment works (optional).

## Deep Reinforcement Learning Algorithms

### Policy Gradient Methods
Optimize the policy directly to maximize rewards.

**PPO (Proximal Policy Optimization)**
The industry standard for continuous control in robotics.
- **Stability**: Prevents large, destructive policy updates.
- **Sample Efficiency**: Reuses data for multiple training steps.

```python
# PPO Update (Concept)
def ppo_update(policy, value_net, batch):
    # Calculate advantages
    advantages = calculate_gae(batch['rewards'], batch['values'])
    
    # Policy loss (clipped surrogate objective)
    ratio = torch.exp(new_log_probs - old_log_probs)
    surr1 = ratio * advantages
    surr2 = torch.clamp(ratio, 1-eps, 1+eps) * advantages
    policy_loss = -torch.min(surr1, surr2).mean()
    
    # Value loss
    value_loss = mse_loss(value_net(states), returns)
    
    # Backpropagate
    total_loss = policy_loss + 0.5 * value_loss
    optimizer.step(total_loss)
```

### Off-Policy Methods
Re-use past experiences stored in a replay buffer.
- **SAC (Soft Actor-Critic)**: Maximizes reward + entropy (randomness) for robust exploration.
- **DQN (Deep Q-Network)**: For discrete action spaces (less common in manipulation).

## Robotic RL Environments

### OpenAI Gym Interface
Standard API for RL environments.

```python
import gym

class RobotEnv(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(7,))
        self.observation_space = gym.spaces.Box(low=-inf, high=inf, shape=(20,))
        
    def reset(self):
        # Reset robot to initial state
        return initial_state
        
    def step(self, action):
        # Apply action to robot
        self.robot.apply_action(action)
        
        # Observe new state
        next_state = self.robot.get_state()
        
        # Calculate reward
        reward = self.compute_reward(next_state)
        
        # Check termination
        done = self.check_termination(next_state)
        
        return next_state, reward, done, {}
```

### Isaac Gym (Preview) / Isaac Lab
Massively parallel simulation on GPU.
- **Physics on GPU**: No CPU-GPU bottleneck.
- **Parallel Envs**: Simulate thousands of robots simultaneously.

```python
# Isaac Gym Setup
from isaacgym import gymapi

# Create thousands of environments
num_envs = 4096
envs = []

for i in range(num_envs):
    # Create env instance (very fast on GPU)
    env = gym.create_env(sim, env_lower, env_upper, num_per_row)
    
    # Add robot actor
    actor = gym.create_actor(env, robot_asset, pose, "robot", i, 1)
    envs.append(env)

# Parallel simulation step
gym.simulate(sim)
gym.fetch_results(sim, True)
```

## Reward Engineering

### The Art of Shaping Rewards
Crafting the reward function is the most critical part of RL.

**Sparse Reward**
- +1 for success, 0 otherwise.
- **Problem**: Agent learns nothing if it never succeeds by chance.

**Dense Reward**
- Shaped reward guiding the agent.
- Example for reaching task: `$r = -d_{target} - \lambda ||a||^2$` (Minimize distance and energy).

**Curriculum Learning**
- Start with easy tasks, gradually increase difficulty.

```python
def compute_reward(self, robot_pos, target_pos, actions):
    # Distance penalty
    dist = torch.norm(robot_pos - target_pos, p=2, dim=-1)
    reward_dist = 1.0 / (1.0 + dist**2)
    
    # Action penalty (discourage jerky motion)
    reward_action = -torch.sum(actions**2, dim=-1)
    
    # Success bonus
    reward_success = (dist < 0.05).float() * 10.0
    
    total_reward = reward_dist + 0.01 * reward_action + reward_success
    return total_reward
```

## Sim-to-Real Transfer

### The Reality Gap
Simulation is perfect; reality is messy. Models trained in sim often fail in real life.

### Domain Randomization (DR)
Randomize physics params to make the policy robust.
- **Dynamics Randomization**: Mass, friction, damping, motor strength.
- **Visual Randomization**: Lighting, textures, camera position.

```python
# Domain Randomization Config
randomization_params = {
    'actor_params': {
        'rigid_body_properties': {
             'mass': {'range': [0.8, 1.2], 'operation': 'scaling'},
             'friction': {'range': [0.5, 1.5], 'operation': 'scaling'}
        },
        'dof_properties': {
             'stiffness': {'range': [0.8, 1.2], 'operation': 'scaling'},
             'damping': {'range': [0.8, 1.2], 'operation': 'scaling'}
        }
    }
}
```

## 🎯 Weekly Project: RL-Based Locomotion

Train a quadruped robot or simple walker to move efficiently:
- **Environment**: Setup Isaac Gym with a terrain environment.
- **Task**: Move forward as fast as possible without falling.
- **Algorithm**: Train using PPO with massive parallelism.
- **Reward Shaping**: Experiment with different reward functions for smooth gait.
- **Transfer**: Validate robustness by changing ground friction.

This project creates a "brain" that learns the physics of walking from scratch!

## Key Takeaways
- **Reinforcement Learning** enables robots to learn complex skills from experience.
- **PPO** is the robust workhorse algorithm for robotic control.
- **Massively parallel simulation** (Isaac Gym) allows training in minutes, not days.
- **Reward engineering** is crucial; "you get what you reward".
- **Domain randomization** bridge the sim-to-real gap by making policies adaptable.

**Congratulations!** You have completed the core technical modules of the Physical AI course. You now possess the knowledge to build, simulate, perceive, and control intelligent robots.