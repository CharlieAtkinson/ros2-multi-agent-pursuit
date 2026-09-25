from setuptools import setup

package_name = 'task2'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='charlieatk',
    maintainer_email='charlieatk@todo.todo',
    description='Task 2 - Single Robot Moving Target',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'predator2_node = task2.predator2_node:main',
            'prey2_node = task2.prey2_node:main',
        ],
    },
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/task2_launch.py']),
    ],
)

