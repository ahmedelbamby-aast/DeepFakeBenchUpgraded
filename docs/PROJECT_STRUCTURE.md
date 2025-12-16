# DeepFakeBench Project Structure

Complete overview of the project directory structure and file organization.

```
DeepFakeBenchUpgraded/
│
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # Project license
├── 📄 pyproject.toml               # Python project configuration
├── 📄 setup.py                     # Package setup script
├── 📄 requirements.txt             # Basic pip requirements
│
├── 📁 deepfakebench/               # Main package directory
│   ├── __init__.py                 # Package initialization
│   ├── train.py                    # Training entry point
│   ├── test.py                     # Testing entry point
│   ├── logger.py                   # Logging utilities
│   │
│   ├── 📁 api/                     # High-level API (NEW)
│   │   ├── __init__.py
│   │   ├── detector.py             # Detector class
│   │   └── utils.py                # API utilities
│   │
│   ├── 📁 config/                  # Configuration files
│   │   ├── __init__.py             # Config module init
│   │   ├── config_manager.py       # Configuration manager (NEW)
│   │   ├── train_config.yaml       # Training configuration
│   │   ├── test_config.yaml        # Testing configuration
│   │   ├── 📁 backbone/            # Backbone configs
│   │   └── 📁 detector/            # Detector configs
│   │       ├── resnet34.yaml
│   │       ├── efficientnetb4.yaml
│   │       ├── xception.yaml
│   │       ├── clip.yaml
│   │       └── ...
│   │
│   ├── 📁 dataset/                 # Dataset implementations
│   │   ├── __init__.py
│   │   ├── abstract_dataset.py     # Base dataset class
│   │   ├── albu.py                 # Augmentation pipelines
│   │   ├── face_utils.py           # Face processing utilities
│   │   ├── ff_blend.py             # FaceForensics blend dataset
│   │   ├── fwa_blend.py            # FWA blend dataset
│   │   ├── sbi_dataset.py          # SBI dataset
│   │   └── ...
│   │
│   ├── 📁 detectors/               # Detection models
│   │   ├── __init__.py             # Registry and imports
│   │   ├── base_detector.py        # Abstract base class
│   │   ├── resnet34_detector.py
│   │   ├── efficientnetb4_detector.py
│   │   ├── xception_detector.py
│   │   ├── clip_detector.py
│   │   ├── f3net_detector.py
│   │   ├── facexray_detector.py
│   │   ├── sbi_detector.py
│   │   └── ...
│   │
│   ├── 📁 networks/                # Network architectures
│   │   ├── __init__.py
│   │   ├── base_backbone.py
│   │   ├── resnet34.py
│   │   ├── efficientnetb4.py
│   │   ├── xception.py
│   │   ├── mesonet.py
│   │   └── ...
│   │
│   ├── 📁 trainer/                 # Training logic
│   │   ├── __init__.py
│   │   └── trainer.py
│   │
│   ├── 📁 metrics/                 # Evaluation metrics
│   │   ├── __init__.py
│   │   ├── base_metrics_class.py
│   │   ├── registry.py
│   │   └── utils.py
│   │
│   ├── 📁 loss/                    # Loss functions
│   │   └── ...
│   │
│   ├── 📁 lib/                     # Utility libraries
│   │   └── ...
│   │
│   ├── 📁 optimizor/               # Custom optimizers
│   │   ├── SAM.py
│   │   └── LinearLR.py
│   │
│   ├── 📁 preprocessing/           # Data preprocessing
│   │   ├── extract_faces.py
│   │   ├── generate_landmarks.py
│   │   └── 📁 dataset_json/        # Dataset metadata
│   │
│   └── 📁 pretrained/              # Pretrained model weights
│       └── ...
│
├── 📁 scripts/                     # Utility scripts (NEW)
│   ├── 📁 install/                 # Installation scripts
│   │   ├── 📁 bash/
│   │   │   └── install.sh          # Linux/macOS installer
│   │   ├── 📁 powershell/
│   │   │   └── install.ps1         # Windows installer
│   │   ├── 📁 conda/
│   │   │   ├── environment.yml     # Full conda env
│   │   │   ├── environment-cpu.yml # CPU-only env
│   │   │   └── environment-minimal.yml
│   │   └── 📁 requirements/
│   │       ├── requirements-base.txt
│   │       ├── requirements-dev.txt
│   │       ├── requirements-full.txt
│   │       ├── requirements-streamlit.txt
│   │       └── requirements-transformers.txt
│   │
│   ├── 📁 data/                    # Data processing scripts
│   │   ├── download_datasets.py
│   │   ├── extract_frames.py
│   │   ├── convert_to_lmdb.py
│   │   └── verify_dataset.py
│   │
│   └── 📁 models/                  # Model utility scripts
│       ├── download_pretrained.py
│       └── export_model.py
│
├── 📁 streamlit_app/               # Streamlit web interface (NEW)
│   ├── app.py                      # Main Streamlit app
│   ├── 📁 components/
│   │   ├── __init__.py
│   │   └── sidebar.py
│   └── 📁 pages/
│       ├── __init__.py
│       ├── home.py
│       ├── detection.py
│       ├── training.py
│       ├── analysis.py
│       └── settings.py
│
├── 📁 api/                         # REST API (NEW)
│   ├── server.py                   # FastAPI server
│   └── models.py                   # Pydantic models
│
├── 📁 docs/                        # Documentation (NEW)
│   ├── INSTALLATION_GUIDE.md
│   ├── DATASET_GUIDE.md
│   ├── MODEL_GUIDE.md
│   ├── API_GUIDE.md
│   └── PROJECT_STRUCTURE.md
│
├── 📁 config/                      # User configuration (NEW)
│   └── local_config.yaml           # Local settings (gitignored)
│
├── 📁 datasets/                    # Data directory
│   ├── 📁 rgb/                     # Raw frame images
│   └── 📁 lmdb/                    # LMDB format data
│
├── 📁 checkpoints/                 # Saved model checkpoints
│
├── 📁 logs/                        # Training logs
│
├── 📁 outputs/                     # Detection outputs
│
├── 📁 cache/                       # Temporary cache
│
├── 📁 analysis/                    # Analysis scripts
│   ├── auc_fromaug.py
│   ├── curve_draw.py
│   ├── tsne.py
│   └── ...
│
├── 📁 figures/                     # Generated figures
│
└── 📁 tests/                       # Unit tests
    ├── test_detectors.py
    ├── test_datasets.py
    └── test_api.py
```

## Key Directories

### `deepfakebench/`
Main Python package containing all core functionality:
- **config/**: Configuration management and YAML configs
- **dataset/**: Dataset loaders and data augmentation
- **detectors/**: All 36+ detection model implementations
- **networks/**: Backbone network architectures
- **trainer/**: Training loop implementation
- **metrics/**: Evaluation metrics and model registry

### `scripts/`
Utility scripts organized by function:
- **install/**: Cross-platform installation scripts
- **data/**: Dataset download and preprocessing
- **models/**: Model management utilities

### `streamlit_app/`
Web interface for interactive deepfake detection:
- Modular page structure
- Reusable components
- Easy to extend

### `docs/`
Comprehensive documentation:
- Installation guides
- API references
- Dataset preparation

## Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python package metadata (PEP 517) |
| `setup.py` | Legacy package installation |
| `requirements.txt` | Basic dependencies |
| `config/local_config.yaml` | Local user settings |

## Data Directories

| Directory | Purpose |
|-----------|---------|
| `datasets/rgb/` | Extracted frame images |
| `datasets/lmdb/` | LMDB-formatted data |
| `checkpoints/` | Saved model weights |
| `logs/` | TensorBoard logs |
| `outputs/` | Detection results |
| `cache/` | Temporary files |

## Adding New Components

### New Detector
1. Create `deepfakebench/detectors/my_detector.py`
2. Register with `@DETECTOR.register_module`
3. Create config `deepfakebench/config/detector/my_detector.yaml`
4. Import in `deepfakebench/detectors/__init__.py`

### New Dataset
1. Create `deepfakebench/dataset/my_dataset.py`
2. Inherit from `DeepfakeAbstractBaseDataset`
3. Create JSON metadata in `preprocessing/dataset_json/`
4. Import in `deepfakebench/dataset/__init__.py`

### New Streamlit Page
1. Create `streamlit_app/pages/my_page.py`
2. Add `render_my_page()` function
3. Register in `streamlit_app/pages/__init__.py`
4. Add navigation in `components/sidebar.py`
