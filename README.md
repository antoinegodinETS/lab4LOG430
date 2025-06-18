# Système Multi-Magasins - Gestion de Caisse (FastAPI / PostgreSQL)

Une application web Python modulaire pour gérer les stocks, ventes et approvisionnements de plusieurs magasins.  
Basée sur **FastAPI**, elle expose des API RESTful et propose une interface web pour la maison mère et les magasins.  
Persistance des données via **PostgreSQL**.

## 🚀 Démarrage rapide

### 1. Installer les dépendances :
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
```

### 2. Initialiser la base de données
Les scripts `init_data.py` et `populate_ventes.py` sont automatiquement exécutés au lancement.  
**Pas besoin de lancer manuellement l'initialisation.**

### 3. Lancer les services avec Docker Compose
```bash
docker-compose up --build
```

- Interface accessible via **http://localhost:8088/123**
- API principale : **http://localhost:8003/docs**

## 🧱 Structure du projet

```
├── .github/workflows/             # CI/CD avec GitHub Actions
├── src/
│   ├── api/                       # Routes FastAPI (REST)
│   ├── interface.py               # Interface web (Jinja2)
│   ├── main.py                    # API centrale
│   ├── magasin/                   # Logique des magasins
│   ├── logistique/                # Logique du centre logistique
│   ├── maison_mere/               # Logique de la maison mère
│   ├── common/                    # Modèles et configuration BD
│   ├── init_data.py               # Init BD
│   └── populate_ventes.py         # Génération de ventes de test
├── templates/                     # HTML Jinja2
├── static/                        # CSS, JS
├── docker-compose.yml
├── Dockerfile
├── prometheus.yml                 # Config Prometheus
├── requirements.txt
└── README.md
```

## ✅ Fonctionnalités principales

- 🏬 Gestion de plusieurs magasins
- 📦 Suivi des stocks (magasin + centre logistique)
- 🔁 Demandes d’approvisionnement avec validation
- 💰 Ventes de produits (avec vérification de stock)
- 📊 Tableau de bord centralisé (performances, rapport)
- 🔍 Visualisation via Prometheus + Grafana
- ⚖️ Répartition de charge avec Nginx
- 🧪 Stress test via `ab` ou `hey`

## 📊 Observabilité

- **Prometheus** (http://localhost:9091)
- **Grafana** (http://localhost:3000, login: `admin` / `admin`)
- **Dashboards** : monitoring d’instances `interface1`, `interface2`, `api`

## ⚙️ CI/CD

Le projet utilise **GitHub Actions** pour :
- Linting avec Flake8
- Exécution des tests
- Build Docker

> Workflow : `.github/workflows/python-app.yml`

## 🔧 Choix techniques

| Technologie     | Rôle                                |
|----------------|-------------------------------------|
| Python 3.12     | Langage principal                   |
| FastAPI         | API REST + Interface HTML           |
| SQLAlchemy      | ORM (accès PostgreSQL)              |
| PostgreSQL      | Base de données relationnelle       |
| Docker          | Conteneurisation                    |
| Grafana         | Visualisation                       |
| Prometheus      | Monitoring                          |
| Nginx           | Répartition de charge               |
| GitHub Actions  | Intégration continue                |

## 🧪 Test de charge

```bash
ab -n 1000 -c 20 http://localhost:8088/123/
```

## 📝 Licence

Ce projet est sous licence **MIT**.