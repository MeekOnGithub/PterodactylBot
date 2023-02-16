import os, time, sys, random, json, nextcord, aiohttp, asyncio, requests
from pydactyl import PterodactylClient
from nextcord.ext import commands, tasks
from nextcord import Intents
from colorama import init
from colorama import Fore, Back, Style
init()



intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

Noone = [" ", "", None]


def checking_files():
	try:
		with open(f"./config.json", "r") as f:
			data = json.load(f)
		token = data["token"]
		prefix = data["prefix"]

		if token in Noone:
			print(f"[{Fore.RED}!{Fore.RESET}] Aucun token n'a était renseigner dans le fichier config.json.")
			exit()
		if prefix in Noone:
			print(f"[{Fore.RED}!{Fore.RESET}] Aucun preifx n'a était renseigner dans le fichier config.json.")
			exit()
		else:
			print(f"[{Fore.GREEN}+{Fore.RESET}] Configuration rempli !")
	except Exception as e:
		if e == "FileNotFoundError: [Errno 2] No such file or directory: './config.json'":
			print(f"[{Fore.RED}!{Fore.RESET}] Ficher config.json introuvable.")
			exit()
		else:
			print(f"[{Fore.RED}!{Fore.RESET}] Une erreur est survenue : {str(e)}")



checking_files()
with open(f"./config.json", "r") as f:
	data = json.load(f)
token = data["token"]
prefix = data["prefix"]


bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None, case_insensitive=True)


class ConfigureSrv(nextcord.ui.Modal):
	def __init__(self):
		super().__init__("Configuration du Pterodactyl")  

	 
		self.name = nextcord.ui.TextInput(
			label="Lien du serveur :",
			placeholder="Exemple : https://panel.yourpanel.com",
			min_length=2,
			max_length=100,
		)
		self.add_item(self.name)

		self.description = nextcord.ui.TextInput(
			label="Clé api",
			placeholder="Ta clé api... (https://panel.yourname.com/account/api)",
			min_length=2,
			max_length=100,
		)
		self.add_item(self.description)


	async def callback(self, interaction: nextcord.Interaction) -> None:
		try:
			data = {"domainlink": self.name.value, "apikey": self.description.value}

			await interaction.send("**Serveur configurer avec succés** ! ", ephemeral=True)
			with open(f"./guild/{interaction.guild.id}.json", "w") as f:
				json.dump(data, f)



		except Exception as e:
			await interaction.send("`Une erreur est survenue lors de l'exécution de la commande 💔`", ephemeral=True)
			await interaction.send(f"> {str(e)}")

class Sendcommand(nextcord.ui.Modal):
	def __init__(self, serverid):
		super().__init__("Envoyer une commande sur le serveur")  
		self.serverid = serverid

	 
		self.name = nextcord.ui.TextInput(
			label="Commande",
			min_length=2,
			max_length=50,
		)
		self.add_item(self.name)


	async def callback(self, interaction: nextcord.Interaction) -> None:
		try:
			serveurs = api.client.servers.list_servers()
			api.client.servers.send_console_command(self.serverid, f"{self.name.value}")
			embed = nextcord.Embed(title="Commande envoyer avec succés ✅", description=self.name.value)
			await interaction.send(embed=embed, ephemeral=True)

		except Exception as e:
			await interaction.send("`Une erreur est survenue lors de l'exécution du bouton 💔`", ephemeral=True)
			await interaction.send(f"> {str(e)}")

class StatutButton(nextcord.ui.View):
	def __init__(self, serverid, apikey, domainlink):
		super().__init__()
		self.value = None
		self.serverid = serverid
		self.apikey = apikey
		self.domainlink = domainlink
		self.api = PterodactylClient(self.domainlink, self.apikey)

	@nextcord.ui.button(label="Arrêt 🛑", style=nextcord.ButtonStyle.green)
	async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
		try:
			firstembed = nextcord.Embed(title="Connexion...")
			first = await interaction.send(embed=firstembed, ephemeral=True)

			server_utilization = api.client.servers.get_server_utilization(self.serverid)
			embed=nextcord.Embed(title="Arrêt du serveur \🛑")
			embed.add_field(name="__Statut :__", value="`Hors-Ligne`")
			api.client.servers.send_power_action(serverid, 'stop')

			await interaction.send(embed=embed, ephemeral=True)
		except Exception as e:
			await interaction.send("`Une erreur est survenue lors de l'exécution du bouton \💔`", ephemeral=True)
			await interaction.send(f"> {str(e)}")
	
	@nextcord.ui.button(label="Démmarrer 🟢", style=nextcord.ButtonStyle.green)
	async def strt(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
		try:
			firstembed = nextcord.Embed(title="Connexion...")
			first = await interaction.send(embed=firstembed, ephemeral=True)

			server_utilization = api.client.servers.get_server_utilization(self.serverid)
			embed=nextcord.Embed(title="Démarrage du serveur 🟢")
			embed.add_field(name="__Statut :__", value="`En cours de démmarage`")
			api.client.servers.send_power_action(serverid, 'start')

			await interaction.send(embed=embed, ephemeral=True)
		except Exception as e:
			await interaction.send("`Une erreur est survenue lors de l'exécution du bouton \💔`", ephemeral=True)
			await interaction.send(f"> {str(e)}")
	
	@nextcord.ui.button(label="Envoyer une commande 👥", style=nextcord.ButtonStyle.green)
	async def wl(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
		try:
			modal = Sendcommand()
			await interaction.response.send_modal(modal)
		except Exception as e:
			await interaction.send("`Une erreur est survenue lors de l'exécution du bouton \💔`", ephemeral=True)
			await interaction.send(f"> {str(e)}")

@bot.command()
async def information(ctx, serverid):
	try:
		if os.path.exists(f"./guild/{ctx.guild.id}.json"):
			firstembed = nextcord.Embed(title="Connexion...")
			first = await ctx.send(embed=firstembed)

			with open(f'./guild/{ctx.guild.id}.json', 'r') as f:
				data = json.load(f)

			apikey = data['apikey']
			domainlink = data["domainlink"]

			api = PterodactylClient(domainlink, apikey)
		
			while True:
				server_utilization = api.client.servers.get_server_utilization(serverid)
			
				embed = nextcord.Embed(title="Panel Du Serveur")
			
			
				if server_utilization["current_state"] == "offline":
					embed.add_field(name="**Statut** : ", value="`🔴 Hors-ligne`")
				elif server_utilization["current_state"] == "running":
					embed.add_field(name="**Statut** : ", value="`🟢 En ligne`")
				elif server_utilization["current_state"] == "starting":
					embed.add_field(name="**Statut** : ", value="`🟠 Démmarage`")
				else:
					embed.add_field(name="**Statut** : ", value="`Inconnu`")
			
			
				if "resources" in server_utilization:
					resources = server_utilization["resources"]
					if "memory_bytes" in resources:
						embed.add_field(name="**Mémoire** : ", value=f"{resources['memory_bytes'] / 1024 / 1024:.2f} Mo")
					if "cpu_absolute" in resources:
						embed.add_field(name="**CPU** : ", value=f"{resources['cpu_absolute']} %")
					if "disk_bytes" in resources:
						embed.add_field(name="**Disque** : ", value=f"{resources['disk_bytes'] / 1024 / 1024:.2f} Mo")
					if "network_rx_bytes" in resources:
						embed.add_field(name="**Réseau (Rx)** : ", value=f"{resources['network_rx_bytes'] / 1024 / 1024:.2f} Mo")
					if "network_tx_bytes" in resources:
						embed.add_field(name="**Réseau (Tx)** : ", value=f"{resources['network_tx_bytes'] / 1024 / 1024:.2f} Mo")
					if "uptime" in resources:
						uptime = resources["uptime"]
						hours, remainder = divmod(uptime, 3600)
						minutes, seconds = divmod(remainder, 60)
						embed.add_field(name="**Uptime** : ", value=f"{hours}h {minutes}m {seconds}s")

					log_file = api.client.servers.files.get_file_contents(serverid, "logs/latest.log")
				if log_file is not None:
					lines = log_file.content.decode('utf-8').splitlines()
					logs = "\n".join(lines[-3:])
					embed.add_field(name="**Logs** : ", value=f"```{logs}```", inline=False)
				else:
					embed.add_field(name="**Ressources** : ", value="Non disponible")
			
				view = StatutButton(serverid)		

			
				await first.edit(embed=embed, view=view)
				await asyncio.sleep(10) 
		else:
			try:
				embed=nextcord.Embed(title="Configuration Pterodactyl requise \🛑")
				embed.add_field(name="_**Pour résouldre ce probléme**_", value=f"```Utiliser la commande : /configptero```")
				await ctx.send(embed=embed)
			except Exception as e:
				await ctx.send("Une erreur est survenue lors de l'exécution de la commande.")
				await ctx.send(f"> ```{str(e)}```")
	except Exception as e:
		await ctx.send("Une erreur est survenue lors de l'exécution de la commande.")
		await ctx.send(f"> ```{str(e)}```")

@bot.slash_command(
	name="configptero", 
	description="Configure the server settings for Pterodactyl")
async def configptero(interaction: nextcord.Interaction, arg: str = ""):
    try:
        if arg == "again":
            modal = ConfigureSrv()
            await interaction.response.send_modal(modal)
            await interaction.send("Merci de bien suivre les intructions sur la fênetre qui vient d'apparaitre !", ephemeral=True)

        if os.path.exists(f"./guild/{interaction.guild.id}.json"):
            embed = nextcord.Embed(title="Votre serveur est déjà configuré \🛑", description=f"Si tu souhaites refaire la configuration, \n Essaye : {prefix}configptero again ")
            await interaction.send(embed=embed)
        else:
        	if arg in Noone:
        		await interaction.send(f"> **Votre argument : `Rien` est invalide !**")
        	else:
        		await interaction.send(f"> **Votre argument : `Rien` est invalide !**")
    except Exception as e:
        await interaction.send("Une erreur est survenue lors de l'exécution de la commande.")
        await interaction.send(f"> ```{str(e)}```")

@bot.listen("on_ready")
async def on_ready():
	try:
		print(f"[{Fore.GREEN}+{Fore.RESET}] Connectée en tant que : {Fore.CYAN}{bot.user.name}{Fore.RESET}")
	except Exception as e:
		print(f"[{Fore.RED}!{Fore.RESET}] Une erreur est survenue : {str(e)}")
bot.run(token)