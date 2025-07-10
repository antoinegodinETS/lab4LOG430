from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common.database import get_db
from maison_mere import services as mm_services
from schemas.rapport_schemas import RapportVentes, ChiffreAffaires, Tendance
from common.cache import cache

router = APIRouter(prefix="/api/v1/maison-mere", tags=["Maison Mère"])

@router.get("/rapport-ventes", response_model=RapportVentes)
async def rapport_ventes(db: Session = Depends(get_db)):
    # Vérifier si le rapport est dans le cache
    cached_report = await cache.get("rapport-ventes")
    if cached_report:
        return cached_report

    # Si non, générer le rapport
    report = mm_services.generer_rapport_ventes()

    # Mettre le rapport en cache
    await cache.set("rapport-ventes", report, expire=600)  # Expire après 10 minutes
    return report

@router.get("/performance")
def performances(db: Session = Depends(get_db)):
    return mm_services.generer_performances()

@router.put("/produits/{produit_id}")
async def update_produit(produit_id: int, payload: dict, db: Session = Depends(get_db)):
    success = mm_services.mettre_a_jour_produit(produit_id, payload)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    # Invalider le cache du rapport de ventes
    await cache.invalidate("rapport-ventes")
    return {"message": "Produit mis à jour avec succès"}
