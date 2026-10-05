"""
config.py
---------

Configuración global de ThermoLab.

Toda la configuración editable de la aplicación debe
centralizarse aquí.
"""

from pathlib import Path

# ==========================================================
# Información de la aplicación
# ==========================================================

APP_NAME = "ThermoLab"

APP_VERSION = "1.0.0"

APP_AUTHOR = "Diego López"

APP_DESCRIPTION = (
    "Sistema de adquisición y monitoreo "
    "de temperatura para USB-5203."
)

# ==========================================================
# Directorios
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

RESOURCES_DIR = ROOT_DIR / "resources"

ICONS_DIR = RESOURCES_DIR / "icons"

STYLES_DIR = RESOURCES_DIR / "styles"

REPORTS_DIR = ROOT_DIR / "reports"

DATA_DIR = ROOT_DIR / "data"

EXPORT_DIR = DATA_DIR / "export"

LOGS_DIR = ROOT_DIR / "logs"

# ==========================================================
# DAQ
# ==========================================================

DEFAULT_SOURCE = "simulator"

DEFAULT_CHANNELS = 8

DEFAULT_SAMPLE_INTERVAL_MS = 200

SUPPORTED_SAMPLE_INTERVALS_MS = [100, 200, 500, 1000, 2000]

MAX_CHANNELS = 8

# ==========================================================
# Gráficas
# ==========================================================

MAX_HISTORY_POINTS = 3000

AUTO_SCROLL = True

# ==========================================================
# Exportación
# ==========================================================

CSV_SEPARATOR = ";"

EXCEL_SHEET_NAME = "Temperaturas"

# ==========================================================
# Interfaz
# ==========================================================

DEFAULT_THEME = "dark"

WINDOW_WIDTH = 1400

WINDOW_HEIGHT = 850

WINDOW_MIN_WIDTH = 1100

WINDOW_MIN_HEIGHT = 700

# ==========================================================
# Estado
# ==========================================================

SIMULATION_ENABLED = True