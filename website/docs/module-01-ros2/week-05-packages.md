---
title: Week 5 - Package Development
sidebar_position: 5
---

# Week 5: Building Deployable Systems

## From Components to Applications
This final week of Module 1 focuses on packaging your ROS 2 components into complete, deployable applications. You'll learn how to structure code, create launch files, and build systems for distribution.

## ROS 2 Package Structure

### Package Creation
```bash
ros2 pkg create --build-type ament_python --node-name my_robot_node my_robot_pkg
```

### Standard Layout
```
my_robot_pkg/
├── package.xml          # Metadata
├── setup.py            # Build config
├── my_robot_pkg/       # Python source
│   ├── __init__.py
│   └── my_robot_node.py
├── launch/             # Launch files
│   └── robot_launch.py
├── config/             # YAML Configs
│   └── default.yaml
└── test/               # Tests
```

### `package.xml` and `setup.py`
Ensure you define dependencies (`rclpy`, `std_msgs`) and entry points for your nodes so `ros2 run` can find them.

## Advanced Launch File Design

### Modular Launch Architecture
Don't put everything in one file. Use inclusions.

```python title="Complete System Launch"
def generate_launch_description():
    pkg_share = FindPackageShare('my_robot_pkg')
    
    # Sensor Group
    sensor_nodes = GroupAction([
        PushRosNamespace('robot'),
        Node(package='my_robot_pkg', executable='lidar_node')
    ])
    
    # Conditional Logic
    rviz = Node(
        condition=IfCondition(LaunchConfiguration('enable_rviz')),
        package='rviz2', executable='rviz2'
    )
    
    return LaunchDescription([
        sensor_nodes,
        rviz
    ])
```

### Configuration Management
Use YAML files to separate config from code.
```yaml title="config/robot_config.yaml"
robot:
  control:
    max_linear_velocity: 1.0
    safety_enabled: true
```

## Testing and Quality Assurance

:::tip[Testing Levels]
1.  **Unit Tests**: Test individual functions (pytest).
2.  **Integration Tests**: Test node communication.
3.  **Launch Tests**: Test system startup.
:::

```python title="Unit Test Example"
def test_node_initialization(node):
    assert node.get_name() == 'robot_node'
    assert node.get_parameter('max_velocity').value == 1.0
```

## Documentation and Deployment

### README Best Practices
*   **Features**: What does it do?
*   **Installation**: How to build? (`colcon build`)
*   **Usage**: How to run? (`ros2 launch ...`)
*   **API**: Topics, Services, Parameters.

### Docker Deployment
Containerize for reproducibility.
```dockerfile
FROM ros:humble
COPY . /ws/src/
RUN colcon build
ENTRYPOINT ["/ws/install/my_pkg/lib/my_pkg/node"]
```

## 🏆 Weekly Project: Complete ROS 2 Package
Create a professional-grade package including:
*   **Modular Architecture**
*   **Comprehensive Launch System**
*   **YAML Configuration**
*   **Test Suite**
*   **Documentation**

## Module 1 Conclusion
Congratulations! You've mastered the foundational skills of Physical AI communication. The **ROS 2** packages you build here will serve as the backbone for the Digital Twins (Module 2) and Brains (Module 3) to come.