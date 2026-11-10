import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

#des intents par défaut suffisent pour les commandes slash et les boutons
intents = discord.Intents.default()


class MonBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        #charge l'extension orders
        try:
            await self.load_extension("orders")
            print("Extension 'orders' chargée !")
        except Exception as e:
            print(f"Erreur lors du chargement de 'orders' : {e}")

        #synchronise les commandes slash
        try:
            await self.tree.sync()
            print("Commandes synchronisées !")
        except Exception as e:
            print(f"Erreur lors de la synchronisation : {e}")


bot = MonBot()


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} !")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Erreur : Aucun token trouvé dans le .env")
    else:
        bot.run(token)