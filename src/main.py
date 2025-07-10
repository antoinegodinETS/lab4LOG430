# from common.database import init_db


# if __name__ == "__main__":
#     init_db()
#     print("✅ Base de données initialisée avec succès.")

# src/main.py

import subprocess
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from api import magasin_api, maison_mere_api, logistique_api
from interface import app as interface_app  # 👈 si interface.py contient app = FastAPI()

# Configuration du logging structuré
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Multi-Magasins - LOG430")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrumentation Prometheus
Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Requête entrante : {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Réponse sortante : {response.status_code} pour {request.url}")
    return response

app.include_router(magasin_api.router)
app.include_router(logistique_api.router)
app.include_router(maison_mere_api.router)

# ✅ Route racine qui affiche toutes les routes
@app.get("/123")
def list_routes():
    return {
        "routes": [
            {"path": route.path, "methods": list(route.methods), "name": route.name}
            for route in app.routes if isinstance(route, APIRoute)
        ]
    }

@app.on_event("startup")
def startup_event():
    logger.info("Démarrage de l'application...")
    try:
        subprocess.run(["python", "init_data.py"], check=True)
        subprocess.run(["python", "populate_ventes.py"], check=True)
        logger.info("Scripts exécutés avec succès.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erreur dans l'exécution d'un script : {e}")


