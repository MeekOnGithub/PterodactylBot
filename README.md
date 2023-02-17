
# PteroBot 🐱‍🐉

Bot discord qui permet de gérer son panel pterodactyl depuis discord


Non Fini !


## Fonctionnalité 

```
✨ Peut être utiliser dans plusieurs serveurs
🎈 Configuration simple, rapide, depuis discord (Pterodactyl)
🎉 Instruction et aide pour le téléchargement et la configuration
```
Commandes :

```
📖 Information - Permet de gérer le serveur et savoir le taux de ram utiliser, poids du serveur, les derniers logs (Only Minecraft), envoyer une commande etc...

🔨 ConfigPtero - Permet de configurer l'api key et le nom de domaine du panel grace a une interface modal

📩 (Non Ajouter) UpFiles - Permet d'envoyer des fichiers depuis discord

🔮 (Non Ajouter) Lisrv - Permet de lister les serveurs et leur information en un seul embed ou plusiers 

Et autres, suggestion seront dans les issues...
```



## Guide d'installation

Voici les instructions pour télécharger le projet à l'aide de Git.

```bash
  git clone https://github.com/MeekOnGithub/PterodactylBot.git
  cd PterodactylBot
```

Téléchargement des modules néccesaires 

```bash
  pip install -r requirements.txt
```

Lancement du projet

```bash
  python3 main.py
```

## Configuration

Pour configurer le bot, il faudra un token et un prefix

`Il faudra remplir le fichier CONFIG.json`

Comment obtenir un token : 

Pour créer un Bot Discord, allez sur le [Portail de développeur ](https://discord.com/developers/applications/) Discord, cliquez sur “New Application”, puis sur l’onglet “Bot” et appuyez sur “Add Bot”. Définissez les droits du bot, puis cliquez sur "RESET TOKEN".

## Erreurs

Si vous ne trouvez pas votre erreur ici, merci de créer un issue 

1 - Dossier ou fichier introuvable
```
[!] Une erreur est survenue : [Errno 2] No such file or directory: './config.json'
Traceback (most recent call last):
  File "C:\Users\Zaidorox\Desktop\InxoBot\main.py", line 44, in <module>
    with open(f"./config.json", "r") as f:
FileNotFoundError: [Errno 2] No such file or directory: './config.json'
```

```
[!] Une erreur est survenue : [Errno 2] No such file or directory: './guild'
Traceback (most recent call last):
  File "C:\Users\Zaidorox\Desktop\InxoBot\main.py", line 44, in <module>
    with open(f"./config.json", "r") as f:
FileNotFoundError: [Errno 2] No such file or directory: './guild'
```
Il s'agit du fait que le fichier config.json ou le dossier guild n'est pas présent, merci de le retélécharger !

2 - Api Key / Lien de nom de domaine du panel invalide

```
Invalid URL '(lien)/api/client/servers/hello/resources': No schema supplied. Perhaps you meant http://(lien)/api/client/servers/hello/resources?
````

Il s'agit du fait que le l'api key et le lien du nom de domaine que vous avez donnez et invalide

⚠ - N'oubliez pas le `https://` ou le `https://` devant le nom de domaine 

Pour obtenir une api key, vous pouvez vous rediriger ici : 
- https://panel.votrelien.com/account/api




Merci pour de me soutenir ici : [Paypal](https://paypal.me/envoieundonbatard.com)

