# src/api/magasin_api.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common.database import get_db
from magasin import services as magasin_services
from schemas.stock_schemas import StockMagasinOut
from common.cache import cache

router = APIRouter(prefix="/api/v1/magasins", tags=["Magasins"])


@router.get("/{magasin_id}/stock", response_model=list[StockMagasinOut])
async def get_stock(magasin_id: int, db: Session = Depends(get_db)):
    # Vérifier si les données sont dans le cache
    cached_stock = await cache.get(f"magasin:{magasin_id}:stock")
    if cached_stock:
        return cached_stock

    # Si non, récupérer les données depuis la base de données
    stock = magasin_services.consulter_stock_magasin(magasin_id)

    # Mettre les données en cache
    await cache.set(f"magasin:{magasin_id}:stock", stock, expire=300)  # Expire après 5 minutes
    return stock

@router.post("/{magasin_id}/produits/{produit_id}/vente")
def vendre(magasin_id: int, produit_id: int, quantite: int, db: Session = Depends(get_db)):
    return magasin_services.vendre_produit(magasin_id, produit_id, quantite)
