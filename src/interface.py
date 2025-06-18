from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from magasin.services import (
    consulter_stock_magasin, performances_magasin, generer_performances_magasin, vendre_produit
)
from logistique.services import (
    consulter_stock_logistique, creer_demande_approvisionnement,
    approvisionner_magasin
)




from maison_mere.services import generer_rapport_ventes
from magasin.models import Produit
from logistique.models import DemandeApprovisionnement
from common.database import SessionLocal

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    db = SessionLocal()
    stock = consulter_stock_logistique()
    demandes = db.query(DemandeApprovisionnement).filter_by(statut="en_attente").all()
    db.close()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stock": stock,
        "demandes": demandes,
        "result": None   # 👈 ajoute ceci
    })



@app.get("/rapport", response_class=HTMLResponse)
def afficher_rapport(request: Request):
    data = generer_rapport_ventes()
    return templates.TemplateResponse("rapport.html", {"request": request, "data": data})


@app.get("/performances", response_class=HTMLResponse)
def afficher_performances(request: Request):
    data = generer_performances_magasin()
    return templates.TemplateResponse("performances.html", {"request": request, "result": data})


@app.get("/maj_produit", response_class=HTMLResponse)
def afficher_formulaire_maj(request: Request):
    db = SessionLocal()
    produits = db.query(Produit).all()
    db.close()
    return templates.TemplateResponse("maj_produit.html", {"request": request, "produits": produits})


@app.post("/maj_produit", response_class=HTMLResponse)
def mettre_a_jour_produit(request: Request, produit_id: int = Form(...), nom: str = Form(...), prix: float = Form(...), description: str = Form(...)):
    db = SessionLocal()
    produit = db.query(Produit).filter_by(id=produit_id).first()
    if produit:
        produit.nom = nom
        produit.prix = prix
        produit.description = description
        db.commit()

    produits = db.query(Produit).all()
    db.close()
    return templates.TemplateResponse("maj_produit.html", {
        "request": request,
        "message": "Produit mis à jour avec succès.",
        "produits": produits
    })


@app.get("/demande_appro", response_class=HTMLResponse)
def afficher_demandes(request: Request):
    db = SessionLocal()
    demandes = db.query(DemandeApprovisionnement).filter_by(statut="en_attente").all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "demandes": demandes})


@app.post("/valider_demande", response_class=HTMLResponse)
def valider_demande(request: Request, demande_id: int = Form(...)):
    db = SessionLocal()
    demande = db.query(DemandeApprovisionnement).get(demande_id)

    if demande:
        approvisionner_magasin(demande.produit_id, demande.quantite, demande.magasin_id)
        demande.statut = "validee"
        db.commit()

    # Recharger les données mises à jour
    stock = consulter_stock_logistique()
    demandes = db.query(DemandeApprovisionnement).filter_by(statut="en_attente").all()
    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "stock": stock,
        "demandes": demandes,
        "result": "Demande validée avec succès."
    })



@app.post("/execute", response_class=HTMLResponse)
async def execute_action(request: Request):
    db = SessionLocal()
    form_data = await request.form()
    action = form_data.get("action")
    section = form_data.get("section", None)
    demandes = db.query(DemandeApprovisionnement).filter_by(statut="en_attente").all()


    result = None
    stock_magasin = None

    try:
        if action == "rapport":
            return RedirectResponse(url="/rapport", status_code=303)

        elif action == "performances":
            result = performances_magasin()

        elif action == "reapprovisionnement":
            produit_id = int(form_data.get("produit_id"))
            quantite = int(form_data.get("quantite"))
            magasin_id = int(form_data.get("magasin_id"))
            creer_demande_approvisionnement(magasin_id, produit_id, quantite)
            return RedirectResponse(url="/", status_code=303)

        elif action == "approvisionner":
            produit_id = int(form_data.get("produit_id"))
            quantite = int(form_data.get("quantite"))
            result = approvisionner_magasin(produit_id, quantite)

        elif action == "consulter_stock_magasin":
            magasin_id = int(form_data.get("magasin_id"))
            stock_magasin = consulter_stock_magasin(magasin_id)
        
        elif action == "vendre_produit":
            produit_id = int(form_data.get("produit_id"))
            quantite = int(form_data.get("quantite"))
            magasin_id = int(form_data.get("magasin_id"))
            result = vendre_produit(magasin_id, produit_id, quantite)


        else:
            result = "Action non reconnue."

    except Exception as e:
        result = f"Erreur : {str(e)}"

    stock = consulter_stock_logistique()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "stock": stock,
        "stock_magasin": stock_magasin,
        "active_section": section,
        "demandes": demandes
    })
