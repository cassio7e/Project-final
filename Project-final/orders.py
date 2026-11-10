import discord
from discord import app_commands
from discord.ext import commands, tasks

import animals as data
import storage_json as storage
from utils import add_xp, jauge_case

URL_IMAGE_KILL = "https://th.bing.com/th/id/OIP.9bnPbPjv-Gk2QkijD2Eo9gHaE8?w=258&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3"
ID_SALON_ANNONCES = 1567454599949062185


def creer_embed_profil(pet: dict, action_nom: str = "") -> discord.Embed:
    infos_species = data.SPECIES.get(pet["espece"], {"label": pet["espece"], "image": ""})
    xp_requise = pet["niveau"] * 100

    embed = discord.Embed(
        title=f"Profil de {pet['nom']}",
        description=(
            f"Espèce : {infos_species.get('label', pet['espece'])}\n"
            f"Niveau : {pet['niveau']} (XP : {pet['xp']}/{xp_requise})"
        ),
        color=discord.Color.gold(),
    )
    embed.add_field(name="Faim", value=jauge_case(pet["faim"]), inline=False)
    embed.add_field(name="Bonheur", value=jauge_case(pet["bonheur"]), inline=False)
    embed.add_field(name="Énergie", value=jauge_case(pet["energie"]), inline=False)
    embed.add_field(name="Propreté", value=jauge_case(pet["proprete"]), inline=False)

    if action_nom:
        actions_dict = getattr(data, "ACTIONS_IMAGES", {}).get(pet["espece"], {})
        image_action = actions_dict.get(action_nom)
        if image_action:
            embed.set_image(url=image_action)
    elif infos_species.get("image"):
        embed.set_image(url=infos_species["image"])

    return embed


async def annoncer_montee_niveau(guild: discord.Guild, user: discord.User | discord.Member, pet: dict) -> None:
    if not guild:
        return

    salon = guild.get_channel(ID_SALON_ANNONCES)
    if salon is None:
        try:
            salon = await guild.fetch_channel(ID_SALON_ANNONCES)
        except Exception:
            return

    if isinstance(salon, discord.TextChannel):
        embed = discord.Embed(
            title=" Level up !",
            description=(
                f"Félicitations à {user.mention} !\n"
                f"Son animal {pet['nom']} vient d'atteindre le Niveau {pet['niveau']} !"
            ),
            color=discord.Color.gold(),
        )
        await salon.send(embed=embed)


class PetActionView(discord.ui.View):
    def __init__(self, owner_id: int):
        super().__init__(timeout=180)
        self.owner_id = owner_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Ce n'est pas ton animal ! Tu ne peux pas interagir avec lui.",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.button(label="Nourrir", style=discord.ButtonStyle.success)
    async def bouton_nourrir(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        pet = storage.get_pet(self.owner_id)
        if not pet:
            await interaction.response.send_message("Animal introuvable.", ephemeral=True)
            return

        if pet["faim"] >= 100:
            await interaction.response.send_message(f"{pet['nom']} n'a plus faim !", ephemeral=True)
            return

        pet["faim"] = min(100, pet["faim"] + 25)
        pet["proprete"] = max(0, pet["proprete"] - 5)
        _, lvl_up = add_xp(pet, 10)
        storage.update_pet(self.owner_id, pet)

        embed = creer_embed_profil(pet, action_nom="manger")
        await interaction.response.edit_message(embed=embed, view=self)

        if lvl_up and interaction.guild:
            await annoncer_montee_niveau(interaction.guild, interaction.user, pet)

    @discord.ui.button(label="Jouer", style=discord.ButtonStyle.primary)
    async def bouton_jouer(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        pet = storage.get_pet(self.owner_id)
        if not pet:
            await interaction.response.send_message("Animal introuvable.", ephemeral=True)
            return

        if pet["energie"] < 20:
            await interaction.response.send_message(f"{pet['nom']} est trop fatigué pour jouer !", ephemeral=True)
            return

        pet["bonheur"] = min(100, pet["bonheur"] + 20)
        pet["faim"] = max(0, pet["faim"] - 15)
        pet["energie"] = max(0, pet["energie"] - 20)
        pet["proprete"] = max(0, pet["proprete"] - 15)
        _, lvl_up = add_xp(pet, 25)
        storage.update_pet(self.owner_id, pet)

        embed = creer_embed_profil(pet, action_nom="jouer")
        await interaction.response.edit_message(embed=embed, view=self)

        if lvl_up and interaction.guild:
            await annoncer_montee_niveau(interaction.guild, interaction.user, pet)

    @discord.ui.button(label="Dormir", style=discord.ButtonStyle.secondary)
    async def bouton_dormir(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        pet = storage.get_pet(self.owner_id)
        if not pet:
            await interaction.response.send_message("Animal introuvable.", ephemeral=True)
            return

        pet["faim"] = max(0, pet["faim"] - 10)
        pet["energie"] = min(100, pet["energie"] + 45)
        storage.update_pet(self.owner_id, pet)

        embed = creer_embed_profil(pet, action_nom="dormir")
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Laver", style=discord.ButtonStyle.primary)
    async def bouton_laver(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        pet = storage.get_pet(self.owner_id)
        if not pet:
            await interaction.response.send_message("Animal introuvable.", ephemeral=True)
            return

        if pet["proprete"] >= 100:
            await interaction.response.send_message(f"{pet['nom']} est déjà tout propre !", ephemeral=True)
            return

        pet["proprete"] = min(100, pet["proprete"] + 40)
        pet["bonheur"] = min(100, pet["bonheur"] + 10)
        pet["energie"] = max(0, pet["energie"] - 5)
        _, lvl_up = add_xp(pet, 15)
        storage.update_pet(self.owner_id, pet)

        embed = creer_embed_profil(pet, action_nom="douche")
        await interaction.response.edit_message(embed=embed, view=self)

        if lvl_up and interaction.guild:
            await annoncer_montee_niveau(interaction.guild, interaction.user, pet)


class TamagotchiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.baisse_temps_automatique.start()

    def cog_unload(self) -> None:
        self.baisse_temps_automatique.cancel()

    @tasks.loop(minutes=10)
    async def baisse_temps_automatique(self) -> None:
        try:
            all_pets = storage._load_data()
            if not all_pets:
                return

            modifie = False
            for pet in all_pets.values():
                if not isinstance(pet, dict):
                    continue

                pet["faim"] = max(0, pet.get("faim", 100) - 5)
                pet["energie"] = max(0, pet.get("energie", 100) - 1)

                if pet.get("xp", 0) > 0:
                    pet["xp"] = max(0, pet["xp"] - 2)

                modifie = True

            if modifie:
                storage._save_data(all_pets)

        except Exception as e:
            print(f"[ERREUR BOUCLE] : {e}")

    @baisse_temps_automatique.before_loop
    async def before_baisse_temps(self) -> None:
        await self.bot.wait_until_ready()

    @app_commands.command(name="tamagotchi", description="Adopte ton animal de compagnie !")
    @app_commands.choices(
        species=[
            app_commands.Choice(name="Capybara", value="capybara"),
            app_commands.Choice(name="Chien", value="chien"),
            app_commands.Choice(name="Chat Noir", value="chat_noir"),
            app_commands.Choice(name="Chauve-Souris", value="chauve_souris"),
        ]
    )
    async def tamagotchi(
        self,
        interaction: discord.Interaction,
        species: app_commands.Choice[str],
        name: str,
    ) -> None:
        user_id = interaction.user.id

        if storage.get_pet(user_id) is not None:
            await interaction.response.send_message("Tu as déjà adopté un animal !", ephemeral=True)
            return

        pet_name = name.strip()
        if not pet_name:
            await interaction.response.send_message("Le prénom de ton animal ne peut pas être vide.", ephemeral=True)
            return

        try:
            pet = storage.create_pet(user_id, nom=pet_name, espece=species.value)
        except ValueError:
            await interaction.response.send_message("Tu as déjà un animal !", ephemeral=True)
            return

        embed = creer_embed_profil(pet)
        embed.title = f"BRAVO, TU AS ADOPTÉ {pet['nom']} !"
        view = PetActionView(owner_id=user_id)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="profil", description="Affiche la fiche et les besoins de ton Tamagotchi.")
    async def profil(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        pet = storage.get_pet(user_id)
        if pet is None:
            await interaction.response.send_message("Aucun animal n'a encore été adopté. Utilise `/tamagotchi` !", ephemeral=True)
            return

        view = PetActionView(owner_id=user_id)
        embed = creer_embed_profil(pet)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="kill", description="Fais disparaître ton Tamagotchi actuel.")
    async def kill(self, interaction: discord.Interaction) -> None:
        user_id = interaction.user.id
        pet = storage.get_pet(user_id)

        if pet is None:
            await interaction.response.send_message("Tu n'as aucun animal à abandonner !", ephemeral=True)
            return

        nom_animal = pet.get("nom", "ton animal")
        if storage.delete_pet(user_id):
            embed = discord.Embed(
                title="Adieu...",
                description=f"{nom_animal} est parti vers de nouveaux horizons...\nTu peux en adopter un nouveau avec `/tamagotchi` !",
                color=discord.Color.dark_grey(),
            )
            embed.set_image(url=URL_IMAGE_KILL)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Erreur lors de la suppression.", ephemeral=True)

    @app_commands.command(name="bonjour", description="Fais apparaître ton Tamagotchi actuel.")
    async def bonjour(self, interaction: discord.Interaction) -> None:
        user = interaction.user
        pet = storage.get_pet(user.id)

        if pet:
            embed = creer_embed_profil(pet)
            embed.title = f"Bon retour {user.display_name} !"
            view = PetActionView(owner_id=user.id)
            await interaction.response.send_message(content=f"Bienvenue {user.mention} !", embed=embed, view=view)
        else:
            embed = discord.Embed(
                title=f"Bienvenue {user.display_name} !",
                description=f"Bienvenue {user.mention} !\nTu n'as pas encore de Tamagotchi. Utilise `/tamagotchi` pour en adopter un !",
                color=discord.Color.green(),
            )
            if user.display_avatar:
                embed.set_thumbnail(url=user.display_avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="regles", description="Affiche la liste des commandes.")
    async def regles(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="Guide des Commandes Tamagotchi",
            description="Voici comment utiliser les commandes principales :",
            color=discord.Color.teal(),
        )
        embed.add_field(name="🥚 /tamagotchi [espece] [name]", value="Adopte un animal de compagnie !", inline=False)
        embed.add_field(name="📋 /profil", value="Affiche la fiche avec les boutons interactifs (Nourrir, Jouer, Dormir, Laver).", inline=False)
        embed.add_field(name="👋 /bonjour", value="Salue le serveur avec ton animal.", inline=False)
        embed.add_field(name="⚠️ /kill", value="Supprime ton animal pour en recommencer un.", inline=False)
        embed.set_footer(text="Astuce : La faim et l'énergie baissent automatiquement toutes les 10 minutes !")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TamagotchiCog(bot))