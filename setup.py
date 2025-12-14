"""
DeepfakeBench: A Comprehensive Benchmark of Deepfake Detection
Upgraded for PyTorch 2.x and Python 3.8+ compatibility

Original authors: Zhiyuan Yan, Yong Zhang, Xinhang Yuan, Siwei Lyu, Baoyuan Wu
Upgraded by: Ahmed ElBamby

This package provides:
- 36+ deepfake detection models
- Unified training and evaluation framework
- Support for 9+ benchmark datasets
- Modern PyTorch 2.x compatibility
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='deepfakebench',
    version='2.0.0',
    author='Zhiyuan Yan, Ahmed ElBamby',
    author_email='ahmedelbamby1102003@gmail.com',
    description='A Comprehensive Benchmark of Deepfake Detection - Upgraded for PyTorch 2.x',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded',
    project_urls={
        'Bug Tracker': 'https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues',
        'Documentation': 'https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/blob/main/README.md',
        'Original Repository': 'https://github.com/SCLBD/DeepfakeBench',
    },
    packages=find_packages(include=['deepfakebench', 'deepfakebench.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ],
    python_requires='>=3.7',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov',
            'black',
            'flake8',
        ],
        'transformers': [
            'transformers>=4.30.2',
            'tokenizers>=0.11,<0.14',
            'regex',
        ],
        'all': [
            'loralib',
            'filterpy',
            'simplejson',
            'fvcore',
        ],
    },
    entry_points={
        'console_scripts': [
            'deepfakebench-train=deepfakebench.train:main',
            'deepfakebench-test=deepfakebench.test:main',
        ],
    },
    include_package_data=True,
    package_data={
        'deepfakebench': ['config/**/*.yaml', 'pretrained/**/*'],
    },
    zip_safe=False,
    keywords='deepfake detection computer-vision deep-learning pytorch face-forgery',
)
