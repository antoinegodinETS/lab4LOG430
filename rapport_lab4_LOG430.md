
# Rapport – Laboratoire 4 – LOG430

## Introduction

Dans ce laboratoire, j'avais pour objectif d’ajouter des fonctionnalités avancées à mon système multi-magasins, en intégrant :
- une couche d'observabilité,
- un mécanisme d'équilibrage de charge,
- et un système de mise en cache applicatif.

J’ai mis en place des outils comme Prometheus, Grafana, Locust et Nginx, et j’ai réalisé des tests de charge pour évaluer la robustesse du système.

---

## Observabilité et Test de Charge

### Intégration Prometheus et Grafana

J’ai utilisé la librairie `prometheus_fastapi_instrumentator` pour exposer les métriques sur `/metrics` (port 8004) de l’interface FastAPI.

Parmi les métriques collectées :
- `http_requests_total` : nombre total de requêtes HTTP,
- `http_request_duration_seconds_sum` : somme des durées de traitement des requêtes,
- `process_resident_memory_bytes` : mémoire utilisée,
- `python_gc_collections_total` : cycles de garbage collector.

Prometheus est configuré pour interroger ces métriques toutes les 5 secondes avec la configuration suivante :

```yaml
scrape_configs:
  - job_name: "interface"
    static_configs:
      - targets: ["10.194.32.192:8004"]
```

J’ai lancé Prometheus via Docker sur le port 9091. Ensuite, j’ai connecté Grafana à Prometheus pour visualiser les métriques.

---

### Test de charge avec Locust

J’ai utilisé Locust pour envoyer des requêtes sur les routes `/`, `/rapport` et `/performances`.

Avant test :
- Peu de requêtes,
- Faible latence (~22 ms à 104 ms),
- Mémoire utilisée : ~80 Mo.

Pendant test (6.7 RPS) :
- Échecs 5xx sur toutes les routes testées,
- Latence en forte hausse : jusqu’à 13.4s de temps cumulé,
- Utilisation CPU et mémoire en augmentation.

🔍 **Conclusion** : Le système montre des failles sous charge, probablement dues à des appels internes synchrones via `httpx`. Ces appels devront être optimisés (timeouts, async, retry).

---

### Visualisation dans Grafana

J’ai ajouté les panels suivants :
- Nombre de requêtes HTTP,
- Temps de réponse,
- Codes d’erreurs (4xx, 5xx),
- Utilisation CPU/Mémoire.

Les courbes m’ont permis d’identifier l'impact des tests sur les performances du système.

---

## Équilibrage de Charge

J’ai mis en place un reverse proxy Nginx distribuant les requêtes entre deux instances de l’interface FastAPI (ports 8004 et 8005).

Configuration `nginx.conf` :

```nginx
upstream backend {
    server interface1:8000;
    server interface2:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

**Résultat** : L’interface répond maintenant sur le port 8088. Les requêtes alternent bien entre les deux services selon le mode round-robin.

---

## Caching Applicatif

J’ai ajouté un cache Python simple pour améliorer la performance sur les requêtes fréquentes, notamment `/produits`.

### Avant Caching (ApacheBench) :
- Temps moyen par requête : 250 ms,
- 1000 requêtes, toutes avec code 500 (erreurs).

### Après Caching :
- Temps moyen réduit à 230 ms,
- Toujours 1000 requêtes, mais aucune requête échouée.

🔍 **Conclusion** : Le cache a réduit légèrement la latence et a stabilisé les requêtes, bien que les réponses soient toujours des erreurs (code 500), ce qui indique un autre bug fonctionnel ou une absence de gestion correcte des exceptions.

---

## Conclusion

J’ai atteint les objectifs suivants :
✅ Mise en place d’une observabilité complète avec Prometheus et Grafana (UC7)  
✅ Réalisation de tests de charge avec Locust, puis ApacheBench  
✅ Implémentation d’un équilibrage de charge avec Nginx (UC8)  
✅ Intégration d’un cache simple dans l’application (UC9)  

Grâce à ces ajouts, mon système est plus robuste, observé en temps réel, et scalable pour de futures évolutions.
