---
sidebar_position: 2
title: Humanoid Robotics Fundamentals
---

# Humanoid Robotics Fundamentals

Humanoid robots are designed to resemble the human body structure, typically featuring a head, torso, two arms, and two legs. This form factor allows them to operate in environments built for humans (stairs, doors, tools).

## Kinematics and Dynamics

*   **Forward Kinematics**: Calculating the position of the end-effector (hand/foot) based on joint angles.
*   **Inverse Kinematics (IK)**: Determining the joint angles needed to reach a specific position.
*   **Dynamics**: Understanding the forces (gravity, coriolis, inertia) acting on the robot.

## Locomotion

Bipedal locomotion is inherently unstable. It requires active balancing.

### Zero Moment Point (ZMP)

The ZMP is a point on the ground where the net tipping moment is zero. For stable walking, the ZMP must remain within the support polygon (the area covered by the feet).

## Manipulation

Humanoid manipulation involves not just arm movement but whole-body control. To lift a heavy box, a robot must adjust its stance and center of mass, just like a human.

## Perception for Humanoids

Humanoids rely on:
*   **LiDAR**: For mapping.
*   **Depth Cameras**: For obstacle avoidance.
*   **IMUs**: For balance and orientation.
