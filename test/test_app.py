import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from common.database import init_db, SessionLocal
from magasin.models import Magasin, Produit, StockMagasin
from maison_mere.models import Vente
from logistique.models import DemandeApprovisionnement, StockLogistique
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import MetaData

Base = declarative_base(metadata=MetaData(schema="lab2_schema"))

@pytest.fixture(scope="function")
def setup_database():
    # Réinitialise la base de données avant chaque test
    session = SessionLocal()
    session.query(DemandeApprovisionnement).delete()
    session.query(Vente).delete()
    session.query(StockMagasin).delete()
    session.query(StockLogistique).delete()
    session.query(Produit).delete()
    session.commit()
    session.close()
    init_db()  # Réinitialiser la structure de la base de données
    yield
    # Nettoyage après chaque test
    session = SessionLocal()
    session.query(DemandeApprovisionnement).delete()
    session.query(Vente).delete()
    session.query(StockMagasin).delete()
    session.query(StockLogistique).delete()
    session.query(Produit).delete()
    session.commit()
    session.close()

def test_ajout_produit(setup_database):
    session = SessionLocal()
    produit = Produit(nom="TestProduit", prix=10.0, description="Produit de test")
    session.add(produit)
    session.commit()

    produits = session.query(Produit).all()
    assert len(produits) == 1
    assert produits[0].nom == "TestProduit"
    session.close()

def test_enregistrement_vente(setup_database):
    session = SessionLocal()

    # Ajout du magasin requis
    magasin = Magasin(nom="Magasin Test", quartier="Centre-ville")
    session.add(magasin)
    session.commit()

    # Ajout du produit
    produit = Produit(nom="ProduitVente", prix=5.0, description="Produit pour vente")
    session.add(produit)
    session.commit()

    # Ajout du stock lié au magasin créé
    stock = StockMagasin(magasin_id=magasin.id, produit_id=produit.id, quantite=10)
    session.add(stock)
    session.commit()

    # Ajout d'une vente liée au même magasin et produit
    vente = Vente(magasin_id=magasin.id, produit_id=produit.id, quantite=3, montant=15.0)
    session.add(vente)
    session.commit()

    # Mise à jour de la quantité
    stock.quantite -= vente.quantite
    session.commit()

    stock_apres_vente = session.query(StockMagasin).filter_by(produit_id=produit.id).first()
    assert stock_apres_vente.quantite == 7
    session.close()

def test_consulter_stock_logistique(setup_database):
    session = SessionLocal()
    produit = Produit(nom="ProduitLogistique", prix=20.0, description="Produit logistique")
    session.add(produit)
    session.commit()

    stock_logistique = StockLogistique(produit_id=produit.id, quantite=50)
    session.add(stock_logistique)
    session.commit()

    stock = session.query(StockLogistique).filter_by(produit_id=produit.id).first()
    assert stock.quantite == 50
    session.close()