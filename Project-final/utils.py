def jauge_case(valeur: int) -> str:
    #Génère une barre visuelle de 5 cases sous forme d'emojis pour une valeur de 0 à 100.
    valeur = max(0, min(100, valeur))
    nbr_verts = valeur // 20
    nbr_gris = 5 - nbr_verts
    return f"{'🟩' * nbr_verts}{'⬜' * nbr_gris} ({valeur}/100)"


def add_xp(pet: dict, montant: int) -> tuple[str, bool]:
    #Ajoute de l'XP à un animal et gère la montée de niveau avec le surplus d'XP.
    pet["xp"] = pet.get("xp", 0) + montant
    pet["niveau"] = pet.get("niveau", 1)
    xp_requise = pet["niveau"] * 100

    montee_niveau = False
    while pet["xp"] >= xp_requise:
        pet["xp"] -= xp_requise
        pet["niveau"] += 1
        xp_requise = pet["niveau"] * 100
        montee_niveau = True

    if montee_niveau:
        return f"Bravo ! **{pet['nom']}** passe au niveau **{pet['niveau']}** !", True

    return f"+{montant} XP ({pet['xp']}/{xp_requise})", False