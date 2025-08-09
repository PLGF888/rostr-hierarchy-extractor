# 👤 Extracteur de Hiérarchie 

Ce projet Python effectue une extraction automatique de la hiérarchie des employés à partir d’un lien de la plateforme interne  à l’aide de **Selenium**.

---

## 🚀 Fonctionnalités

- Accède à la page d’un employé et parcourt récursivement toute sa hiérarchie de subordonnés.
- Extrait les informations suivantes :
  - Nom et superviseur
  - Poste (*title*) et lieu d’affectation (*location*)
  - Informations organisationnelles :
    - Code de société
    - Domaine d’activité
    - Zone de personnel
    - Unité organisationnelle
    - Centre de coûts
    - Type d’employé
- Stocke les données dans :
  - `hierarchie.csv` — données extraites
  - `visitados.json` — URLs déjà visitées (pour éviter les répétitions)
- Validation du lien initial avec `inquirer`
- Prise en charge de la reprise automatique en cas d’interruption

---

## 🛠️ Technologies utilisées

- Python 3.10+
- Selenium
- Inquirer
- pretty_errors
- re (expressions régulières)
- datetime
- csv / json

---

## 💻 Instructions d’exécution

### 1. Cloner le projet

```bash
git clone https://github.com/votreutilisateur/hierarchie-rostr.git
cd hierarchie-rostr
```

### 2. Créer et activer un environnement virtuel

```bash
uv venv
uv pip install -r requirements.txt
```

### 3. Lancer le script principal

```bash
python hierarchie-rostr.py
```

Vous serez invité à saisir le lien de la page initiale (par exemple, celle d’un responsable hiérarchique).

---

## 📁 Structure du projet

```text
📦hierarchie-rostr
 ┣ 📁.venv                  # Environnement virtuel (optionnel)
 ┣ 📜hierarchie-rostr.py    # Script principal
 ┣ 📜hierarchie.csv         # Données extraites
 ┣ 📜visitados.json         # Liens déjà visités
 ┣ 📜README.md              # Ce fichier
 ┗ 📜requirements.txt       # Dépendances du projet
```

---

## 📝 Exemple de sortie CSV

| Nom             | Superviseur      | Poste             | Lieu d’affectation                     | Code société | Centre de coûts | ... |
|------------------|-------------------|--------------------|------------------------------------------|----------------|-------------------|-----|
| Jean Dupont      | Marie Martin       | Analyste           | Workforce Labor Systems & Insights       | 1111           | 123456            | ... |
| Marie Martin     | SANS SUPERVISEUR  | Responsable        | HR Systems                               | 1111           | 654321            | ... |

---

## 🔄 Reprise automatique

En cas d’interruption (ex. : délai expiré, plantage), le script lit `visitados.json` et **ignore** les URLs déjà traitées lors du redémarrage.

---

## ❓ FAQ

### ➤ Puis-je minimiser le navigateur pendant l’exécution ?
Oui, Selenium continuera à fonctionner normalement.

### ➤ Puis-je verrouiller l’écran ou suspendre l’ordinateur ?
**Non.** Le navigateur cessera de fonctionner. Gardez l’écran actif.

### ➤ Et si le site expire après 30 minutes ?
Le script sauvegarde en continu :
- les données (`hierarchie.csv`)
- les liens visités (`visitados.json`)

Vous pourrez ainsi relancer le script et reprendre là où il s’était arrêté.

---

## 🙌 Remerciements

Développé avec l’aide de ChatGPT 💬 et votre participation active !  
Outil idéal pour l’analyse organisationnelle, les exports RH, et l’exploration des données internes.

---

## 📄 Licence

Distribué sous licence MIT.
