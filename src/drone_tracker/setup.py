from setuptools import find_packages, setup

package_name = 'drone_tracker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sc',
    maintainer_email='2451366311@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'vision_node = drone_tracker.vision_node:main',
            'state_estimator = drone_tracker.state_estimator:main',
            'flight_control = drone_tracker.flight_control:main',
            'gimbal_controller = drone_tracker.gimbal_controller:main',
        ],
    },   
)
