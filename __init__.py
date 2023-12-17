import discord
import requests
from understar.system import lib
from typing import List
from PIL import Image
import io
import base64
import json

Lib = lib.App()

url = "http://127.0.0.1:7860"

payload_json = {
    "alwayson_scripts" : {
        "API payload" :{
            "args" : []
        },
        "Extra options" :{
            "args" : []
        },
        "Refiner" :{
            "args" : [
                False, 
                "sd_xl_refiner_1.0_0.9vae.safetensors [8d0ce6c016]", 
                0.8
            ]
        },
        "Seed" :{
            "args" : [
                -1,
                False,
                -1,
                0,
                0,
                0
            ]
        },
        "Style Selector for SDXL 1.0" :{
        "args" : [
            True,
            False,
            False,
            False,
            "Photographique"
            ]
        }
    },
    "prompt": "",
    "steps": 5,
    "sampler_name": "DPM++ 2M Karras",
    "width" : 512,
    "height" : 512
}

style = [
    "base",
    "Modèle 3D",
    "Film Analogique",
    "Anime",
    "Cinématographique",
    "Bande Dessinée",
    "Argile Artisanale",
    "Art Numérique",
    "Améliorer",
    "Art Fantastique",
    "Style Isométrique",
    "Dessin au Trait",
    "Lowpoly",
    "Néon Punk",
    "Origami",
    "Photographique",
    "Pixel Art",
    "Texture",
    "Publicité",
    "Photographie Culinaire",
    "Immobilier",
    "Abstrait",
    "Cubiste",
    "Graffiti",
    "Hyperréalisme",
    "Impressionniste",
    "Pointillisme",
    "Art Pop",
    "Psychédélique",
    "Renaissance",
    "Steampunk",
    "Surréaliste",
    "Typographie",
    "Aquarelle",
    "Jeu de Combat",
    "GTA",
    "Super Mario",
    "Minecraft",
    "Pokémon",
    "Rétro Arcade",
    "Jeu Rétro",
    "Jeu de RPG Fantastique",
    "Jeu de Stratégie",
    "Street Fighter",
    "Legend of Zelda",
    "Architectural",
    "Disco",
    "Paysage Onirique",
    "Dystopique",
    "Conte de Fées",
    "Gothique",
    "Grunge",
    "Horreur",
    "Minimaliste",
    "Monochrome",
    "Nautique",
    "Spatial",
    "Vitraux",
    "Mode Techwear",
    "Tribal",
    "Zentangle",
    "Collage",
    "Découpe en Papier Plate",
    "Kirigami",
    "Papier Maché",
    "Quilling en Papier",
    "Collage en Papier Découpé",
    "Boite d'Ombres en Découpe de Papier 3D",
    "Découpe Empilée en Papier",
    "Découpe épaisse en Papier Empilée",
    "Alien",
    "Film Noir",
    "HDR",
    "Longue Exposition",
    "Noir Néon",
    "Silhouette",
    "Tilt-Shift"
]

    

models = []

class ModelTransformer(discord.app_commands.Transformer):

    @classmethod
    async def transform(self, interaction: discord.Interaction, value: str, /) -> discord.Color:
        return value

    @classmethod
    async def autocomplete(self, interaction: discord.Interaction, value: str) -> List[discord.app_commands.Choice[str]]:
        choices: List[discord.app_commands.Choice] = []
        for m in models:
            choices.append(discord.app_commands.Choice(name=m.get("model_name"), value=m.get("title")))
        return choices[:25]

def get_model_list():
    response = requests.get(url=f'{url}/sdapi/v1/sd-models')
    r = response.json()
    return r

def gen_image(prompt, steps=25):
    payload=payload_json
    payload["prompt"] = prompt
    payload["steps"] = steps

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    if response.status_code == 200:
        r = response.json()

        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        image.save('output.png')
    else:
        print(response.text)


@Lib.event.event()
async def on_ready():
    global models
    models = get_model_list()

@Lib.app.slash(name="text2image", description="génère une image par IA")
async def remove_manga(ctx: discord.Interaction, model: ModelTransformer, channel: discord.ForumChannel):
    pass

if __name__=="__main__":
    pass
    #gen_image("Dreamscape bird's eye view shot, by Marta Bevacqua, we see a beautiful birch forest and a lake, the lighting atmosphere is very beautiful, the light is very soft, everything is very bright, the weather is very cloudy, very mystical, it is rainy, we are in the north of Europe, The scene is reminiscent of a music video, in Vogue style, a very high quality photo shoot, full shot, art cinematic scene, --ar 2:3 --style raw --v 5.2")