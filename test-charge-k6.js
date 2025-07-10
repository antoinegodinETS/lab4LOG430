import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 }, // Monter à 50 utilisateurs simultanés
    { duration: '1m', target: 100 }, // Monter à 100 utilisateurs simultanés
    { duration: '30s', target: 0 },  // Descendre à 0 utilisateurs
  ],
};

const BASE_URL = 'http://localhost:8004/api/v1';

export default function () {
  // Consultation simultanée des stocks de plusieurs magasins
  const magasinIds = [1, 2, 3, 4, 5]; // Exemple d'IDs de magasins
  magasinIds.forEach((id) => {
    const res = http.get(`${BASE_URL}/magasins/${id}/stock`);
    check(res, {
      'Stock consulté avec succès': (r) => r.status === 200,
    });
  });

  // Génération de rapports consolidés
  const rapportRes = http.get(`${BASE_URL}/maison-mere/rapport-ventes`);
  check(rapportRes, {
    'Rapport généré avec succès': (r) => r.status === 200,
  });

  // Mise à jour de produits à forte fréquence
  const produitId = 1; // Exemple d'ID de produit
  const payload = JSON.stringify({
    nom: 'Produit mis à jour',
    prix: 99.99,
  });
  const headers = { 'Content-Type': 'application/json' };
  const updateRes = http.put(`${BASE_URL}/maison-mere/produits/${produitId}`, payload, { headers });
  check(updateRes, {
    'Produit mis à jour avec succès': (r) => r.status === 200,
  });

  sleep(1); // Pause entre les requêtes
}