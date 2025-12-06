---
title: Week 4 - Services & Actions
sidebar_position: 4
---

# Week 4: Advanced Communication Patterns

## Building Distributed Robotic Systems
This week focuses on the practical implementation of ROS 2's core communication patterns. You'll learn how to design and implement nodes that communicate effectively to create complex behaviors.

## Deep Dive into ROS 2 Nodes

### Node Lifecycle and Best Practices
Proper node design ensures reliability and performance.

```python title="Advanced Node Initialization"
class AdvancedNode(Node):
    def __init__(self):
        super().__init__('advanced_node')
        
        # Concurrent execution groups
        self.timer_group = MutuallyExclusiveCallbackGroup()
        self.service_group = MutuallyExclusiveCallbackGroup()
        
        self.create_publishers()
        self.create_subscriptions()
        
    def create_publishers(self):
        self.pose_publisher = self.create_publisher(PoseStamped, '/robot_pose', 10)
```

### Executors
ROS 2 supports different execution models:
*   **SingleThreadedExecutor**: Default, simple.
*   **MultiThreadedExecutor**: concurrently runs callbacks.

## Topics: Asynchronous Data Streaming

### Custom Message Types
Define standard messages for your specific domain (e.g., `CustomSensor.msg`).

### Topic Monitoring
Create monitor nodes to track system health.
```python
def update_topic_stats(self, topic_name, msg):
    # Track frequency and latency
    pass
```

## Services: Synchronous Communication

### Service Design Patterns
Services are great for:
1.  **Parameter Query**: Get/Set configuration.
2.  **Validation**: Check if a goal is valid before executing.

```python title="Motion Planning Service"
def plan_path_callback(self, request, response):
    # Validate
    if not self.validate_pose(request.start):
        response.success = False
        return response
    
    # Plan
    path = self.generate_path(request.start, request.goal)
    response.path = path
    response.success = True
    return response
```

## Actions: Complex Task Execution

:::warning[Why Actions?]
Unlike services, **Actions** are non-blocking and provide feedback. Use them for navigation, manipulation, or anything taking > 1 second.
:::

### Action Server Implementation
```python
class ComplexTaskAction(Node):
    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing task...')
        
        # Provide Feedback
        for i in range(10):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return Result()
            
            goal_handle.publish_feedback(Feedback(progress=i*10))
            time.sleep(1)
            
        goal_handle.succeed()
        return Result(success=True)
```

## Integration Patterns

### Complete Robotic System
A typical robot structure:
*   **Perception Node**: Publishes sensor data.
*   **Processing Node**: Fuses data.
*   **Planning Node**: Service for paths.
*   **Control Node**: Action for execution.

## 🏆 Weekly Project: Integrated ROS 2 System
Build a complete system demonstrating all patterns:
*   **Perception**: Camera/Lidar/IMU publishers.
*   **Planning**: Path planning service.
*   **Control**: Motion action interface.
*   **Monitoring**: System health tracker.

## Key Takeaways
1.  Choose patterns carefully: **Topics** (Stream), **Services** (Query), **Actions** (Task).
2.  **QoS** is crucial for real-time performance.
3.  **Error handling** ensures reliability.