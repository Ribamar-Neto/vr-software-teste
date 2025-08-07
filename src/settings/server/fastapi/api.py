from fastapi import FastAPI

from src.settings.server import api_settings

app = FastAPI(
    title=api_settings.title,
    description=api_settings.description,
    debug=api_settings.debug,
    swagger_ui_parameters={'defaultModelsExpandDepth': -1, 'syntaxHighlight': False},
)
