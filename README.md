# Système Multi-Magasins - Gestion de Caisse (FastAPI / PostgreSQL)

Une application web Python modulaire pour gérer les stocks, ventes et approvisionnements de plusieurs magasins. Basée sur **FastAPI**, elle expose des API RESTful et propose une interface web pour la maison mère et les magasins. Persistance des données via **PostgreSQL**.

---

## 🚀 Démarrage rapide

### **1. Installer les dépendances :**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd source
```

## 2. Initialiser la base de données

Les scripts `init_data.py` et `populate_ventes.py` sont automatiquement exécutés au lancement.  
**Pas besoin de lancer manuellement l'initialisation.**

---

## 3. Lancer l’API principale (routes REST)

```bash
uvicorn main:app --port 8003 --reload
```

## 4. Lancer l’interface web (FastAPI + Jinja2)

```bash
uvicorn interface:app --port 8004 --reload
```

## 5. Accéder à l’application

- **Interface Web** : [http://127.0.0.1:8004](http://127.0.0.1:8004)
- **Swagger UI (API)** : [http://127.0.0.1:8003/docs](http://127.0.0.1:8003/docs)
- **ReDoc (alternative Swagger)** : [http://127.0.0.1:8003/redoc](http://127.0.0.1:8003/redoc)

---

## 🧱 Structure du projet

```bash
├── .github/
│   └── workflows/               # CI/CD avec GitHub Actions
├── docs/                        # Documentation (ADR, UML, besoins)
├── src/
│   ├── api/                     # Routes FastAPI (maison_mere, magasin, logistique)
│   ├── interface.py             # Interface HTML + Jinja2
│   ├── main.py                  # Point d’entrée principal de l’API REST
│   ├── common/                  # Initialisation, configuration et modèles partagés
│   ├── maison_mere/             # Logique maison mère
│   ├── logistique/              # Logique du centre logistique
│   ├── magasin/                 # Logique des magasins
│   ├── database.py              # Configuration SQLAlchemy
│   ├── init_data.py             # Script d’initialisation des données
│   └── populate_ventes.py       # Génération de données de vente (démo)
├── templates/                   # Fichiers HTML (interface utilisateur)
├── static/                      # Fichiers CSS, JS, images
├── tests/                       
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
```
## ✅ Fonctionnalités principales

- 🏪 Gestion multi-magasins  
- 📦 Suivi des stocks  
- 🛒 Ventes de produits  
- 🔁 Demandes d’approvisionnement avec validation  
- 📊 Tableau de bord centralisé (maison mère)  
- 🔐 Séparation des responsabilités : magasin / logistique / maison mère  
- 🧪 Initialisation automatisée des données (dev/démo)  
- 📚 Documentation Swagger intégrée  

---

## ⚙️ CI/CD

Le projet utilise **GitHub Actions** pour automatiser les étapes suivantes :

- Installation des dépendances  
- Exécution des tests unitaires  
- Initialisation de la base de données  
- Build de l’image Docker  

> **Fichier CI/CD** : `.github/workflows/python-app.yml`

---

## 🔧 Choix techniques

| Technologie     | Rôle                                 |
|----------------|--------------------------------------|
| Python 3.12     | Langage principal                    |
| FastAPI         | Framework web (API REST & Jinja2)   |
| SQLAlchemy      | ORM pour PostgreSQL                 |
| PostgreSQL      | Base de données relationnelle       |
| Jinja2          | Rendu HTML côté serveur             |
| httpx           | Appels HTTP entre modules internes  |
| Docker          | Conteneurisation                    |
| GitHub Actions  | Intégration continue                |

---

## 📝 Licence

Ce projet est distribué sous licence **MIT**.  
Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
