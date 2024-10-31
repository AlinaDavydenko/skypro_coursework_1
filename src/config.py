from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
file_path = ROOT_DIR.joinpath("data", "operations.xlsx")
settings_path = ROOT_DIR.joinpath("user_settings.json")
