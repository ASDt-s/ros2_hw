# ROS 2 Turtlesim Homework (小海龟二次开发)

本项目基于 ROS 2 Humble，实现了 turtlesim 仿真节点的自动避障、多运动模式切换以及自定义键盘遥控功能。

## 依赖项
- ROS 2 Humble
- `turtlesim`
- `example_interfaces`
- `xterm` (用于弹窗运行遥控节点，如需安装请执行 `sudo apt install xterm`)

## 目录结构
```text
ros2_ws/
├── src/
│   └── turtle_hw_pkg/
│       ├── config/                  # YAML 参数配置文件目录
│       │   └── turtle_params.yaml
│       ├── launch/                  # Launch 启动文件目录
│       │   └── turtle_hw.launch.py
│       ├── turtle_hw_pkg/           # Python 源码目录
│       │   ├── __init__.py
│       │   ├── controller.py        # 自动避障与模式切换控制节点
│       │   └── teleop.py            # 自制遥控器节点
│       ├── package.xml
│       └── setup.py
└── README.md
