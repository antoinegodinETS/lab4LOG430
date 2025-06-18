from common.database import SessionLocal
from magasin.models import Produit, StockMagasin
from maison_mere.models import Vente
from sqlalchemy import func

def performances_magasin():
    session = SessionLocal()
    stats = session.query(
        Vente.magasin_id,
        func.sum(Vente.quantite).label("total_ventes")
    ).group_by(Vente.magasin_id).all()
    session.close()
    return [{"magasin_id": r[0], "total_ventes": r[1]} for r in stats]

def generer_performances_magasin():
    return {
        "chiffre_affaires": {
            1: 12345,
            2: 11200,
            3: 8900,
            4: 15000,
            5: 9700,
        },
        "ruptures_stock": [
            {"produit_id": 1, "nom": "Produit A", "magasin_id": 2, "quantite": 2},
            {"produit_id": 2, "nom": "Produit B", "magasin_id": 5, "quantite": 1},
        ],
        "surstock": [
            {"produit_id": 3, "nom": "Produit C", "magasin_id": 1, "quantite": 120},
        ],
        "tendances_hebdo": [
            {"semaine": "Semaine 22", "ventes": [1500, 1800, 2000, 2200, 2100]},
        ]
    }


def consulter_stock_magasin(magasin_id: int):
    session = SessionLocal()
    stock = (
        session.query(StockMagasin, Produit)
        .join(Produit, StockMagasin.produit_id == Produit.id)
        .filter(StockMagasin.magasin_id == magasin_id)
        .all()
    )
    session.close()

    stock_info = [
        {
            "produit_id": produit.id,
            "nom": produit.nom,
            "quantite": stock_entry.quantite
        }
        for stock_entry, produit in stock
    ]
    return stock_info

def vendre_produit(magasin_id: int, produit_id: int, quantite: int) -> str:
    db = SessionLocal()
    
    try:
        stock = db.query(StockMagasin).filter_by(
            magasin_id=magasin_id,
            produit_id=produit_id
        ).first()
        
        for s in stock:
            print(s.produit_id, s.quantite)

        if stock is None:
            return f"Erreur : Le produit {produit_id} n'existe pas dans le stock du magasin {magasin_id}."

        if quantite <= 0:
            return "Erreur : La quantité doit être positive."

        if stock.quantite < quantite:
            return f"Erreur : Stock insuffisant. Disponible : {stock.quantite}, demandé : {quantite}."

        # Mise à jour du stock
        stock.quantite -= quantite
        db.commit()
        return f"✅ Vente réussie de {quantite} unité(s) du produit {produit_id} par le magasin {magasin_id}."

    except Exception as e:
        db.rollback()
        return f"Erreur inattendue : {str(e)}"

    finally:
        db.close()
