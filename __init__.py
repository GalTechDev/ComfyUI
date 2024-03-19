import discord
import requests
from understar.system import lib
from typing import List
from PIL import Image
import io
import base64
import threading

Lib = lib.App()

save_path = ("sd_output", "output.png")

url = "http://127.0.0.1:7860"

prompt = "?"
last_progress = 0
job_count = 0
ctx = None

stack = []

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
                "", 
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
    "negative_prompt": "",
    "steps": 5,
    "sampler_name": "DPM++ 2M Karras",
    "width" : 512,
    "height" : 512
}

style = [
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
    async def transform(self, interaction: discord.Interaction, value: str, /) -> str:
        return value

    @classmethod
    async def autocomplete(self, interaction: discord.Interaction, value: str) -> List[discord.app_commands.Choice[str]]:
        choices: List[discord.app_commands.Choice] = []
        for m in models:
            choices.append(discord.app_commands.Choice(name=m.get("model_name"), value=m.get("title")))
        return choices[:25]
        
class StyleTransformer(discord.app_commands.Transformer):
    @classmethod
    async def transform(self, interaction: discord.Interaction, value: str):
        return value

    @classmethod
    async def autocomplete(self, interaction: discord.Interaction, value: str) -> List[discord.app_commands.Choice[str]]:
        choices: List[discord.app_commands.Choice] = []
        for m in style:
            choices.append(discord.app_commands.Choice(name=m, value=m))
        return choices[:25]

class Prompt(discord.ui.Modal):
    positive = discord.ui.TextInput(
        label='Positive prompt',
        required=False,
        style=discord.TextStyle.long
    )

    negative = discord.ui.TextInput(
        label='Negative prompt',
        required=False,
        style=discord.TextStyle.long,
    )

    def __init__(self, ctx, style, refiner, steps) -> None:
        super().__init__(title='Prompt')
        self.ctx = ctx
        self.style = style
        self.refiner = refiner
        self.steps = steps

    async def on_submit(self, interaction: discord.Interaction):
        global ctx
        ctx = interaction
        await interaction.response.send_message(f'Generating... 0%\n**{self.positive.value}**', ephemeral=True)
        stack.append([self.positive.value, self.negative.value, self.style, self.refiner, self.steps, ctx])
        #await gen_image(self.positive.value, self.negative.value, self.style, self.refiner, self.steps)
        await lib.valide_intaraction(interaction)
        #await interaction.edit_original_response(content=f'**{self.positive.value}**', attachments=[discord.File(Lib.save.get_full_path(save_path[1],save_path[0]))])

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Une erreur est survenu', ephemeral=True)

def get_model_list():
    response = requests.get(url=f'{url}/sdapi/v1/sd-models')
    r = response.json()
    return r

async def update_stak():
    global ctx
    if stack:
        args = stack.pop(0)
        ctx = args.pop()
        threading.Thread(target=gen_image, args=args).start()

def gen_image(p_prompt, n_prompt="", style="base", refiner="", steps=25):
    payload=payload_json
    payload["prompt"] = p_prompt
    payload["negative_prompt"] = n_prompt
    payload["steps"] = steps

    payload["alwayson_scripts"]["Refiner"]["args"][1] = refiner
    payload["alwayson_scripts"]["Style Selector for SDXL 1.0"]["args"][4] = style
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    if response.status_code == 200:
        r = response.json()
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        image.save(Lib.save.get_full_path(save_path[1],save_path[0]))

async def update_progress(): #ctx: discord.Interaction, prompt
    async def download_img():
        img_data = r.get("current_image")
        if img_data:
            image = Image.open(io.BytesIO(base64.b64decode(img_data)))
            #image = image.resize((1024, 1024))
            image.save(Lib.save.get_full_path(save_path[1],save_path[0]))

    async def update_img(ctx, job_no, job_count):
        if Lib.save.existe(save_path[1],save_path[0]):
            if isinstance(ctx, discord.Message):
                await ctx.edit(content=f"Generating... {int((progress-job_no*(1/job_count))/(100/job_count)*100*100)}%\n**{prompt}**", attachments=[discord.File(Lib.save.get_full_path(save_path[1],save_path[0]))])
            elif isinstance(ctx, discord.Interaction):
                await ctx.edit_original_response(content=f"Generating... {int((progress-job_no*(1/job_count))/(100/job_count)*100*100)}%\n**{prompt}**", attachments=[discord.File(Lib.save.get_full_path(save_path[1],save_path[0]))])
        else:
            if isinstance(ctx, discord.Message):
                await ctx.edit(content=f"Generating... {int((progress-job_no*(1/job_count))/(100/job_count)*100*100)}%\n**{prompt}**")
            elif isinstance(ctx, discord.Interaction):
                await ctx.edit_original_response(content=f"Generating... {int((progress-job_no*(1/job_count))/(100/job_count)*100*100)}%\n**{prompt}**")

    global last_progress, ctx, job_count
    if ctx:
        response = requests.get(url = "http://127.0.0.1:7860/sdapi/v1/progress")
        r = response.json()
        progress = r.get("progress")
        state = r.get("state")
        job_no = state.get("job_no")
        if job_no == job_count:
            if progress > last_progress:
                last_progress = progress
                await download_img()
                await update_img(ctx, job_no, state.get("job_count"))
        elif job_no > job_count:
            await update_img(ctx, 1, 1)
            if isinstance(ctx, discord.Message):
                await ctx.edit(content=f"Generating... finished\n**{prompt}**")
            elif isinstance(ctx, discord.Interaction):
                await ctx.edit_original_response(content=f"Generating... finished\n**{prompt}**")
            if job_count < state.get("job_count"):
                ctx = await Lib.client.get_user(608779421683417144).send(f"Generating... 0%\n**{prompt}**")
                last_progress = 0
            job_count=job_no
    else:
        response = requests.get(url = "http://127.0.0.1:7860/sdapi/v1/progress")
        r = response.json()
        job = r.get("job")
        if job != "":
            ctx = await Lib.client.get_user(608779421683417144).send(f"Generating... 0%\n**{prompt}**")
    

@Lib.event.event()
async def on_ready():
    global models
    models = get_model_list()
    if not Lib.save.existe(save_path[0]):
        Lib.save.add_folder(save_path[0])

@Lib.app.slash(name="text2image", description="génère une image par IA")
async def text2image(ctx: discord.Interaction, style: StyleTransformer="base", refiner: ModelTransformer="", steps: int=25):
    await ctx.response.send_modal(Prompt(ctx, style, refiner, steps))

@Lib.app.loop(seconds=15)
async def update():
    print(ctx)
    await update_progress()

@Lib.app.loop(seconds=15)
async def check_stak():
    await update_stak()

if __name__=="__main__":
    pass
    #gen_image("Dreamscape bird's eye view shot, by Marta Bevacqua, we see a beautiful birch forest and a lake, the lighting atmosphere is very beautiful, the light is very soft, everything is very bright, the weather is very cloudy, very mystical, it is rainy, we are in the north of Europe, The scene is reminiscent of a music video, in Vogue style, a very high quality photo shoot, full shot, art cinematic scene, --ar 2:3 --style raw --v 5.2")
    #update_progress()
