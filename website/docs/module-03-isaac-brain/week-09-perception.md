---
title: "Week 9: Perception"
sidebar_position: 2
---

# Week 9: AI-Powered Perception and Manipulation

## Giving Robots the Sense of Sight and Touch

This week transforms your robot from a blind machine into a perceptive agent. We'll explore **AI-powered perception**, enabling robots to identify, locate, and manipulate objects in 3D space. You'll move beyond simple camera feeds to deep learning models that understand the world, creating the bridge between raw sensor data and intelligent action.

## Perception Architectures

### The Perception Pipeline
A typical robotic perception pipeline consists of:

1.  **Data Acquisition**: Capturing data from cameras, LIDAR, and depth sensors.
2.  **Preprocessing**: Noise reduction, filtering, and normalization.
3.  **Feature Extraction**: Identifying key points, edges, and textures.
4.  **Inference**: Running AI models for detection, segmentation, and pose estimation.
5.  **Post-processing**: Tracking, data association, and state estimation.

### Deep Learning for Robotics
Robotics relies on specific neural network architectures:
- **CNNs (Convolutional Neural Networks)**: For image classification and object detection.
- **PointNet/PointNet++**: For 3D point cloud classification and segmentation.
- **Transfomers**: Vision transformers for sequence and attention-based tasks.
- **Graph Neural Networks**: For relationship modeling and scene graphs.

## Object Detection and Segmentation

### YOLO (You Only Look Once)
Real-time object detection essential for fast robot control.

```python
# YOLO inference with PyTorch
import torch

# Load model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Inference
results = model('image.jpg')

# Process results
predictions = results.xyxy[0].cpu().numpy()
for pred in predictions:
    x1, y1, x2, y2, conf, cls = pred
    print(f"Detected class {cls} with confidence {conf} at [{x1}, {y1}, {x2}, {y2}]")
```

### Semantic Segmentation
Classifying every pixel in an image for navigable space detection.

```python
# Semantic segmentation with torchvision
import torchvision.transforms as T
from torchvision.models.segmentation import fcn_resnet50

# Load model
model = fcn_resnet50(pretrained=True).eval()

# Transform input
transform = T.Compose([T.ToTensor(), T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
input_tensor = transform(image).unsqueeze(0)

# Inference
output = model(input_tensor)['out'][0]
prediction = output.argmax(0)
```

## 6D Pose Estimation

### Understanding 6D Pose
To manipulate an object, a robot must know its **6D Pose**:
- **3D Position**: (x, y, z)
- **3D Orientation**: (roll, pitch, yaw) or quaternion

### Pose Estimation Techniques
1.  **Correspondence-Based**: Matching 2D image features to 3D model points (PnP).
2.  **Template-Based**: Matching input against a library of rendered templates.
3.  **Direct Regression**: Neural networks predicting pose directly from images.

```python
# Pose estimation with DenseFusion (pseudo-code)
class PoseEstimator:
    def estimate_pose(self, rgb, depth, mask, cam_K):
        # Extract features
        img_feat = self.cnn(rgb)
        cloud_feat = self.pointnet(depth, mask, cam_K)
        
        # Fuse features
        fused = self.fusion_layer(img_feat, cloud_feat)
        
        # Regress pose
        translation = self.trans_head(fused)
        rotation = self.rot_head(fused)
        confidence = self.conf_head(fused)
        
        return self.refine_pose(translation, rotation, confidence)
```

## Manipulation and Grasping

### Grasp Detection
Identifying viable grasp points on an object.

**GraspNet Architecture**
- Input: Point cloud or RGB-D image.
- Output: Set of 6D grasp poses with quality scores.

```python
# Grasp quality evaluation
def evaluate_grasp(gripper_pose, object_cloud):
    # Check collisions with gripper
    if check_collision(gripper_pose, object_cloud):
        return 0.0
        
    # Check contact points
    contacts = find_contacts(gripper_pose, object_cloud)
    if len(contacts) < 2:
        return 0.0
        
    # Calculate grasp metric (e.g., force closure)
    return calculate_quality(contacts)
```

### Motion Planning for Manipulation
Moving the arm to the grasp pose without collisions.

```python
# MoveIt! 2 planning in Python
from moveit_configs_utils import MoveItConfigsBuilder
from moveit.planning import MoveGroupInterface

# Setup
move_group = MoveGroupInterface("manipulator", "base_link")

# Define target
target_pose = geometry_msgs.msg.Pose()
target_pose.position.x = 0.5
target_pose.position.y = 0.0
target_pose.position.z = 0.5
target_pose.orientation.w = 1.0

# Plan and execute
move_group.set_pose_target(target_pose)
plan = move_group.plan()

if plan.success:
    move_group.execute(plan)
else:
    print("Planning failed!")
```

## Visual Servoing

### Image-Based Visual Servoing (IBVS)
Control robot motion to minimize error in the image plane.

```python
# Simple proportional controller for visual servoing
def update_control(target_pixels, current_pixels, Kp=0.01):
    error = target_pixels - current_pixels
    velocity_cmd = Kp * error
    return velocity_cmd
```

### Position-Based Visual Servoing (PBVS)
Control robot motion based on estimated 3D pose error.

```python
# PBVS control loop
def pose_servoing_loop(target_pose):
    while not reached_target():
        # Estimate current pose
        current_pose = pose_estimator.get_pose()
        
        # Calculate error in 3D
        error = compute_pose_error(target_pose, current_pose)
        
        # Compute velocity command (Cartesian velocity)
        v_cartesian = Kp * error
        
        # Convert to joint velocities using Jacobian pseudoinverse
        J = robot.get_jacobian()
        v_joints = np.linalg.pinv(J) @ v_cartesian
        
        # Send to robot
        robot.set_joint_velocities(v_joints)
```

## Imitation Learning

### Learning from Demonstration (LfD)
Teaching robots by showing them what to do.

1.  **Kinesthetic Teaching**: Physically guiding the robot arm.
2.  **Teleoperation**: Controlling the robot remotely.
3.  **Video Demonstration**: Learning from human videos.

```python
# Behavioral Cloning (BC) Training Loop
def train_bc_policy(demos, policy_network):
    optimizer = torch.optim.Adam(policy_network.parameters())
    
    for epoch in range(num_epochs):
        for state, action in demos:
            # Predict action
            pred_action = policy_network(state)
            
            # Calculate loss (MSE)
            loss = torch.nn.functional.mse_loss(pred_action, action)
            
            # Backpropagate
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

## 🎯 Weekly Project: Intelligent Pick-and-Place

Build a complete pick-and-place system:
- **Perception**: Use a camera to detect objects on a table.
- **Pose Estimation**: Determine position and orientation of target object.
- **Grasp Planning**: Select optimal grasp points.
- **Motion Planning**: Plan collision-free path to grasp object.
- **Execution**: Pick up object and place it in a target container.

This project integrates perception, planning, and control into a cohesive robotic skill.

## Key Takeaways
- **Perception pipelines** convert raw sensor data into meaningful world representations.
- **Object detection and segmentation** identify what acts are in the scene.
- **6D pose estimation** tells the robot exactly where objects are for interaction.
- **Motion planning** moves the robot safely to the target.
- **Visual servoing** provides closed-loop control for precise positioning.

Next week, we'll explore the pinnacle of robotic learning: Reinforcement Learning, where robots learn complex behaviors through trial and error.