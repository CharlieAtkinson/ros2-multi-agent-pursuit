from setuptools import find_packages, setup

package_name = 'task1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/task1_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='charlieatk',
    maintainer_email='charlieatk@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
                'prey_node = task1.prey_node:main',
        	'predator_node = task1.predator_node:main',
        ],
    },
)
