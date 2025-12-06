---
title: Week 3 - Topics & Messages
sidebar_position: 3
---

# Week 3: ROS 2 Fundamentals

## The Communication Backbone
This week marks your transition from conceptual understanding to practical implementation. **ROS 2** (Robot Operating System 2) serves as the communication infrastructure that enables the complex interactions required for Physical AI.

## ROS 2 Architecture: A Distributed Nervous System

### Core Design Principles
ROS 2 is built on modern software engineering principles:
*   🌍 **Distributed**: Components run on different machines or processes
*   ⏱️ **Real-time**: Deterministic communication with quality-of-service guarantees
*   🔒 **Secure**: Built-in encryption and access control
*   🧱 **Modular**: Components can be mixed and matched from different sources

## Key Components

### Nodes: The Building Blocks
Nodes are independent executable processes that perform specific functions.

```python title="Basic Node Structure"
import rclpy
from rclpy.node import Node

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        self.get_logger().info('Sensor node initialized')
        
        # Create a timer for periodic tasks
        self.timer = self.create_timer(1.0, self.timer_callback)
    
    def timer_callback(self):
        # Perform sensor reading and processing
        sensor_data = self.read_sensor()
        self.get_logger().info(f'Sensor reading: {sensor_data}')
```

### Topics: Asynchronous Communication
Topics enable one-to-many communication for streaming data.

:::tip[Publish/Subscribe Pattern]
*   **Publishers** send data out (e.g., Sensor readings).
*   **Subscribers** listen for data (e.g., Controller).
:::

```python title="Publisher Node"
class DataPublisher(Node):
    def __init__(self):
        super().__init__('data_publisher')
        self.publisher_ = self.create_publisher(String, 'sensor_data', 10)
        self.timer = self.create_timer(0.1, self.publish_data)

    def publish_data(self):
        msg = String()
        msg.data = f'Data point {self.counter}'
        self.publisher_.publish(msg)
```

### Quality of Service (QoS)
ROS 2 provides fine-grained control over communication behavior:
*   **Reliability**: Best effort vs. reliable delivery.
*   **Durability**: Volatile vs. transient local storage.
*   **History**: Keep last vs. keep all messages.

```python title="QoS Profile Example"
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=1
)
```

### Services: Synchronous Request-Response
Services enable direct communication between nodes.

```python title="Service Server"
class MathService(Node):
    def __init__(self):
        super().__init__('math_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_callback)
    
    def add_callback(self, request, response):
        response.sum = request.a + request.b
        return response
```

### Actions: Long-Running Tasks
Actions handle complex, interruptible operations (like navigation).

## Debugging and Monitoring

### CLI Tools
*   `ros2 node list` - List active nodes
*   `ros2 topic list` - List topics
*   `ros2 topic echo /topic` - specific topic data
*   `ros2 param get /node param` - Get parameters

### Logging
```python
self.get_logger().info('General information')
self.get_logger().warn('Warning about potential issues')
self.get_logger().error('Error that prevents normal operation')
```

## Best Practices

:::note[Node Design]
*   Keep nodes focused on single responsibilities.
*   Use descriptive names.
*   Handle exceptions gracefully.
:::

:::info[Communication]
*   Use **Topics** for streaming data.
*   Use **Services** for short queries.
*   Use **Actions** for long tasks.
:::

## 🏆 Weekly Project: ROS 2 Communication System
Build a complete ROS 2-based system with:
1.  **Sensor Node**: Publishes simulated sensor data.
2.  **Processing Node**: Subscribes and analyzes.
3.  **Control Node**: Provides services for control.
4.  **Launch File**: Orchestrates all nodes.

## Key Takeaways
1.  ROS 2 enables **distributed, real-time** robotic systems.
2.  Nodes, topics, and services provide **building blocks** for complex behaviors.
3.  **QoS settings** are critical for real-world reliability.