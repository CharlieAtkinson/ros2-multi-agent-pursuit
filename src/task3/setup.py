from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'task4'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # This line tells ROS2 to install your launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='charlieatk',
    maintainer_email='charlieatk@todo.todo',
    description='Task 4 - Multi-Robot Moving Target',
    license='Apache License 2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            # format: 'executable_name = package_name.file_name:main_function'
            'predator4_node = task4.predator4_node:main',
            'prey4_node = task4.prey4_node:main',
        ],
    },
)
