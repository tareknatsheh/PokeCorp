from decouple import config

is_development = int(config("IS_DEVELOPMENT_MODE")) or 0
frontend_folder_name = "frontend_local" if is_development else "frontend"
