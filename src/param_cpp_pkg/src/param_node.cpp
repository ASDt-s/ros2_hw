#include "rclcpp/rclcpp.hpp"
#include <string>

class ParamNode : public rclcpp::Node
{
public:
    ParamNode() : Node("cpp_param_node")
    {
        // 1. 声明参数 (注意：绝对不要声明 use_sim_time！)
        this->declare_parameter("frames.odom", "default_odom");
        this->declare_parameter("frames.baselink", "default_baselink");
        this->declare_parameter("frames.lidar", "default_lidar");
        this->declare_parameter("frames.imu", "default_imu");

        // 2. 获取参数
        bool sim_time = this->get_parameter("use_sim_time").as_bool();
        std::string odom = this->get_parameter("frames.odom").as_string();
        std::string baselink = this->get_parameter("frames.baselink").as_string();
        std::string lidar = this->get_parameter("frames.lidar").as_string();
        std::string imu = this->get_parameter("frames.imu").as_string();

        // 3. 打印
        RCLCPP_INFO(this->get_logger(), "====== 成功读取 YAML 内容 (C++) ======");
        RCLCPP_INFO(this->get_logger(), "use_sim_time: %s", sim_time ? "true" : "false");
        RCLCPP_INFO(this->get_logger(), "frames.odom: %s", odom.c_str());
        RCLCPP_INFO(this->get_logger(), "frames.baselink: %s", baselink.c_str());
        RCLCPP_INFO(this->get_logger(), "frames.lidar: %s", lidar.c_str());
        RCLCPP_INFO(this->get_logger(), "frames.imu: %s", imu.c_str());
        RCLCPP_INFO(this->get_logger(), "======================================");
    }
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ParamNode>();
    rclcpp::spin_some(node); // 打印一次就退出
    rclcpp::shutdown();
    return 0;
}
