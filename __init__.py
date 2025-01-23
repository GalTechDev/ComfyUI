import discord
import requests
from understar.system import lib
from typing import List
import websocket
import json
from threading import Thread
from uuid import uuid4
from random import randint
import asyncio
from io import BytesIO


Lib = lib.App()

config = {}
protocol = "http"
domain = "localhost:8188"

save_path = ("sd_output", "output.png")
tasks = []
queue_remaining = 0
models = []

def data_load():
    global config, protocol, domain
    if not Lib.save.existe("config.json"):
        Lib.save.add_file("config.json")
        Lib.save.write("config.json", data="{}")

    config = Lib.save.json_read("config.json")
    protocol = config.get("protocol", protocol)
    config["protocol"] = protocol

    domain = config.get("domain", domain)
    config["domain"] = domain

    Lib.save.write("config.json", data=json.dumps(config))

#############################################################
#                       Workflow                            #
#############################################################

txt2img_workflow = {
    "client_id": "",
    "prompt": {
        "42": {
            "inputs": {
                "ckpt_name": ""
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "44": {
            "inputs": {
                "seed": 0,
                "steps": 8,
                "cfg": 2,
                "sampler_name": "dpmpp_sde",
                "scheduler": "karras",
                "denoise": 1,
                "model": [
                    "42",
                    0
                ],
                "positive": [
                    "48",
                    0
                ],
                "negative": [
                    "51",
                    0
                ],
                "latent_image": [
                    "47",
                    0
                ]
            },
            "class_type": "KSampler"
        },
        "45": {
            "inputs": {
                "samples": [
                    "44",
                    0
                ],
                "vae": [
                    "42",
                    2
                ]
            },
            "class_type": "VAEDecode"
        },
        "47": {
            "inputs": {
                "width": 1024,
                "height": 1024,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "48": {
            "inputs": {
                "text": "",
                "clip": [
                    "42",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "51": {
            "inputs": {
                "text": "",
                "clip": [
                    "42",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "54": {
            "inputs": {
                "filename_prefix": "",
                "images": [
                    "45",
                    0
                ]
            },
            "class_type": "SaveImage"
        }
    },
    "extra_data": {
        "extra_pnginfo": {
            "workflow": {
                "last_node_id": 54,
                "last_link_id": 130,
                "nodes": [
                    {
                        "id": 42,
                        "type": "CheckpointLoaderSimple",
                        "pos": [
                            -188,
                            -181
                        ],
                        "size": {
                            "0": 315,
                            "1": 98
                        },
                        "flags": {},
                        "order": 0,
                        "mode": 0,
                        "outputs": [
                            {
                                "name": "MODEL",
                                "type": "MODEL",
                                "links": [
                                    113
                                ],
                                "shape": 3,
                                "slot_index": 0
                            },
                            {
                                "name": "CLIP",
                                "type": "CLIP",
                                "links": [
                                    121,
                                    127
                                ],
                                "shape": 3,
                                "slot_index": 1
                            },
                            {
                                "name": "VAE",
                                "type": "VAE",
                                "links": [
                                    117
                                ],
                                "shape": 3,
                                "slot_index": 2
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "CheckpointLoaderSimple"
                        },
                        "widgets_values": [
                            ""
                        ]
                    },
                    {
                        "id": 44,
                        "type": "KSampler",
                        "pos": [
                            656,
                            -157
                        ],
                        "size": {
                            "0": 315,
                            "1": 262
                        },
                        "flags": {},
                        "order": 4,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "model",
                                "type": "MODEL",
                                "link": 113
                            },
                            {
                                "name": "positive",
                                "type": "CONDITIONING",
                                "link": 122
                            },
                            {
                                "name": "negative",
                                "type": "CONDITIONING",
                                "link": 128
                            },
                            {
                                "name": "latent_image",
                                "type": "LATENT",
                                "link": 119
                            }
                        ],
                        "outputs": [
                            {
                                "name": "LATENT",
                                "type": "LATENT",
                                "links": [
                                    116
                                ],
                                "shape": 3,
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "KSampler"
                        },
                        "widgets_values": [
                            879523854994921,
                            "randomize",
                            8,
                            2,
                            "dpmpp_sde",
                            "karras",
                            1
                        ]
                    },
                    {
                        "id": 47,
                        "type": "EmptyLatentImage",
                        "pos": [
                            -185,
                            -25
                        ],
                        "size": {
                            "0": 315,
                            "1": 106
                        },
                        "flags": {},
                        "order": 1,
                        "mode": 0,
                        "outputs": [
                            {
                                "name": "LATENT",
                                "type": "LATENT",
                                "links": [
                                    119
                                ],
                                "shape": 3,
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "EmptyLatentImage"
                        },
                        "widgets_values": [
                            1024,
                            1024,
                            1
                        ]
                    },
                    {
                        "id": 51,
                        "type": "CLIPTextEncode",
                        "pos": [
                            195,
                            -261
                        ],
                        "size": {
                            "0": 422.84503173828125,
                            "1": 164.31304931640625
                        },
                        "flags": {},
                        "order": 3,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "clip",
                                "type": "CLIP",
                                "link": 127
                            }
                        ],
                        "outputs": [
                            {
                                "name": "CONDITIONING",
                                "type": "CONDITIONING",
                                "links": [
                                    128
                                ],
                                "slot_index": 0
                            }
                        ],
                        "title": "Positive Prompt",
                        "properties": {
                            "Node name for S&R": "CLIPTextEncode"
                        },
                        "widgets_values": [
                            ""
                        ]
                    },
                    {
                        "id": 48,
                        "type": "CLIPTextEncode",
                        "pos": [
                            198,
                            -471
                        ],
                        "size": {
                            "0": 422.84503173828125,
                            "1": 164.31304931640625
                        },
                        "flags": {},
                        "order": 2,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "clip",
                                "type": "CLIP",
                                "link": 121
                            }
                        ],
                        "outputs": [
                            {
                                "name": "CONDITIONING",
                                "type": "CONDITIONING",
                                "links": [
                                    122
                                ],
                                "slot_index": 0
                            }
                        ],
                        "title": "Positive Prompt",
                        "properties": {
                            "Node name for S&R": "CLIPTextEncode"
                        },
                        "widgets_values": [
                            ""
                        ]
                    },
                    {
                        "id": 45,
                        "type": "VAEDecode",
                        "pos": [
                            1042,
                            -91
                        ],
                        "size": {
                            "0": 210,
                            "1": 46
                        },
                        "flags": {
                            "collapsed": False
                        },
                        "order": 5,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "samples",
                                "type": "LATENT",
                                "link": 116
                            },
                            {
                                "name": "vae",
                                "type": "VAE",
                                "link": 117
                            }
                        ],
                        "outputs": [
                            {
                                "name": "IMAGE",
                                "type": "IMAGE",
                                "links": [
                                    130
                                ],
                                "shape": 3,
                                "slot_index": 0
                            }
                        ],
                        "properties": {
                            "Node name for S&R": "VAEDecode"
                        }
                    },
                    {
                        "id": 54,
                        "type": "SaveImage",
                        "pos": [
                            1301,
                            -99
                        ],
                        "size": {
                            "0": 315,
                            "1": 58
                        },
                        "flags": {},
                        "order": 6,
                        "mode": 0,
                        "inputs": [
                            {
                                "name": "images",
                                "type": "IMAGE",
                                "link": 130
                            }
                        ],
                        "properties": {},
                        "widgets_values": [
                            ""
                        ]
                    }
                ],
                "links": [
                    [
                        113,
                        42,
                        0,
                        44,
                        0,
                        "MODEL"
                    ],
                    [
                        116,
                        44,
                        0,
                        45,
                        0,
                        "LATENT"
                    ],
                    [
                        117,
                        42,
                        2,
                        45,
                        1,
                        "VAE"
                    ],
                    [
                        119,
                        47,
                        0,
                        44,
                        3,
                        "LATENT"
                    ],
                    [
                        121,
                        42,
                        1,
                        48,
                        0,
                        "CLIP"
                    ],
                    [
                        122,
                        48,
                        0,
                        44,
                        1,
                        "CONDITIONING"
                    ],
                    [
                        127,
                        42,
                        1,
                        51,
                        0,
                        "CLIP"
                    ],
                    [
                        128,
                        51,
                        0,
                        44,
                        2,
                        "CONDITIONING"
                    ],
                    [
                        130,
                        45,
                        0,
                        54,
                        0,
                        "IMAGE"
                    ]
                ],
                "groups": [],
                "config": {},
                "extra": {},
                "version": 0.4
            }
        }
    }
}

img2img_workflow = {}

#############################################################
#                     Other Class                           #
#############################################################

class Task:
    def __init__(self, ctx: discord.Interaction, positive: str, negative: str, model: str, seed: int) -> None:
        self.ctx = ctx
        self.uuid = None
        self.seed = seed
        self.positive = positive
        self.negative = negative
        self.model = model
        self.thread = None

        self.send_prompt()

    def send_prompt(self):
        self.uuid = str(uuid4())
        send_prompt(self.uuid, self.seed, self.model, self.positive, self.negative)

    def get_embed(self, status="", file=None):
        embed = discord.Embed(title=f"**{self.positive}**", description=f"Negative : **{self.negative}**" if self.negative else None)
        embed.add_field(name="Model :", value=self.model.split(".")[0])

        if file: 
            embed.set_image(url="attachment://image.png")
        else:
            embed.set_author(name=status)

        return embed

    async def wait4img(self):
        while True:
            response = requests.get(f"{protocol}://{domain}/view?filename={self.uuid}_00001_.png&type=output")
            if response.status_code == 200:
                response = requests.get(f"{protocol}://{domain}/view?filename={self.uuid}_00001_.png&type=output")
                image = BytesIO(response.content)          
                break
            await asyncio.sleep(1)

        try:
            task = tasks.pop(0)
        except Exception:
            pass

        view = Text2Image_View(ctx=self.ctx, task=task)

        file=discord.File(fp=image, filename='image.png')
        await self.ctx.edit_original_response(embed=self.get_embed(file=file), attachments=[file], view=view)
        
        await update_task()

    async def update_msg(self):
        if tasks[0] is self:
            if not self.thread:
                self.thread = True
                await self.ctx.edit_original_response(embed=self.get_embed("Generating..."))
                await self.wait4img()

        else:
            await self.ctx.edit_original_response(embed=self.get_embed(f"Queue remaining : {queue_remaining}"))

#############################################################
#                       Transformer                         #
#############################################################

class ModelTransformer(discord.app_commands.Transformer):

    @classmethod
    async def transform(self, interaction: discord.Interaction, value: str, /) -> str:
        return value

    @classmethod
    async def autocomplete(self, interaction: discord.Interaction, value: str) -> List[discord.app_commands.Choice[str]]:
        choices: List[discord.app_commands.Choice] = []
        for m in models:
            choices.append(discord.app_commands.Choice(name=m.split(".")[0], value=m))
        return choices[:25]

#############################################################
#                           View                            #
#############################################################  

class Text2Image_View(discord.ui.View):
    def __init__(self, ctx: discord.Interaction, task: Task, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.task = task

        self.regenerate_btn = self.ReGenerate(self.task, emoji="🔄")
        self.add_item(self.regenerate_btn)

    async def on_timeout(self):
        await self.ctx.edit_original_response(view=None)

    class ReGenerate(discord.ui.Button):
        def __init__(self, task: Task, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: str | None = None, disabled: bool = False, custom_id: str | None = None, url: str | None = None, emoji: str | discord.Emoji | discord.PartialEmoji | None = None, row: int | None = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.task = task

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            task = Task(interaction, positive=self.task.positive, negative=self.task.negative, model=self.task.model, seed=gen_seed())
            tasks.append(task)

            await interaction.response.send_message(embed=task.get_embed(f"Queue remaining : {queue_remaining}"), ephemeral=False)
            await update_task()
        
#############################################################
#                           Modal                           #
#############################################################  


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

    def __init__(self, ctx: discord.Interaction, model: str, steps: int) -> None:
        super().__init__(title='Prompt')
        self.model = model
        self.steps = steps

    async def on_submit(self, interaction: discord.Interaction):
        task = Task(interaction, self.positive.value, self.negative.value, self.model, gen_seed())
        await interaction.response.send_message(embed=task.get_embed(f"Queue remaining : {queue_remaining}"), ephemeral=False)
        tasks.append(task)
        await update_task()
        
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"Une erreur est survenu : {error}", ephemeral=True)

#############################################################
#                           ComfyUI                         #
#############################################################

def gen_seed():
    return randint(100000000000000,999999999999999)

def get_model_list():
    info_url = f"http://{domain}/object_info"
    response = requests.get(info_url)
    if response.status_code == 200:
        data = response.json()
        model_list = data.get("CheckpointLoaderSimple", {}).get("input", {}).get("required", {}).get("ckpt_name", [])
        return model_list[0]
    else:
         return []
    
def on_open(idk):
    print("ComfyUI Connected")

def on_message(idk, msg):
    global queue_remaining
    msg = json.loads(msg)
    if msg.get("type") == "status":
        print(f"ComfyUI Message : {msg}")
        queue_remaining = msg["data"]["status"]["exec_info"]["queue_remaining"]

def on_error(idk, e):
    print(f"ComfyUI Error : {e}")

def on_close(idk):
    print("ComfyUI Disconnected")

def send_prompt(uuid: str, seed: int, model: str, positive_prompt: str = "", negative_prompt: str = ""):
    prompt_url = f"http://{domain}/prompt"

    wrk = txt2img_workflow.copy()
    wrk["prompt"]["42"]["inputs"]["ckpt_name"] = model
    wrk["prompt"]["44"]["inputs"]["seed"] = seed
    wrk["prompt"]["48"]["inputs"]["text"] = positive_prompt
    wrk["prompt"]["51"]["inputs"]["text"] = negative_prompt
    wrk["prompt"]["54"]["inputs"]["filename_prefix"] = uuid

    wrk = json.dumps(wrk).encode('utf-8')

    r = requests.post(prompt_url, data=wrk, headers={'Content-Type': 'application/json'})

async def update_task():
    for task in tasks:
        await task.update_msg()

async def updurl(ctx: discord.Interaction, new_domain, new_protocol):
    global domain, protocol
    domain = new_domain
    protocol = new_protocol

    config["domain"] = domain
    config["protocol"] = protocol

    Lib.save.write("config.json", data=json.dumps(config))

    await lib.valide_intaraction(ctx)


#############################################################
#                           Event                           #
#############################################################

@Lib.event.event()
async def on_ready():
    global models

    data_load()

    models = get_model_list()

    ws_url = f"ws://{domain}/ws"
    sws = websocket.WebSocketApp(ws_url, on_open=on_open , on_message=on_message, on_error=on_error, on_close=on_close)
    thread = Thread(target=sws.run_forever)
    thread.start()

    print("ComfyUI ready !")
    print(models)

#############################################################
#                           Slash                           #
#############################################################

@Lib.app.slash(name="text2image", description="Génère une image par IA")
async def text2image(ctx: discord.Interaction, model: ModelTransformer, steps: int=25):
    await ctx.response.send_modal(Prompt(ctx, model, steps))


#############################################################
#                           View                            #
#############################################################

class Updurl_view(discord.ui.View):
    def __init__(self, *, ctx: discord.Interaction, url="", _protocol="", timeout: lib.Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.url = domain
        self._protocol = _protocol

        self.add_item(self.Url_button(view=self, label="Edit domaine" if self.url else "Set domaine", style=discord.ButtonStyle.green if self.url else discord.ButtonStyle.gray))
        self.add_item(self.Protocol_select(view=self, protocol=self._protocol, placeholder="Set protocol"))
        self.add_item(self.Valide_button(view=self, label="Validate", style=discord.ButtonStyle.blurple, disabled=(self.url=="" or self._protocol=="")))

    class Url_button(discord.ui.Button):
        def __init__(self, *, view, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.per_view = view

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await interaction.response.send_modal(Updurl_modal(view=self.per_view, title="URL"))

    class Protocol_select(discord.ui.Select):
        def __init__(self, *, view, protocol, custom_id: str = lib.MISSING, placeholder: lib.Optional[str] = None, min_values: int = 1, max_values: int = 1, options: lib.List[discord.SelectOption] = lib.MISSING, disabled: bool = False, row: lib.Optional[int] = None) -> None:
            self.per_view = view
            self.keys = ["http", "https"]
            self.protocol = protocol
            options = [discord.SelectOption(label=key, default=True if self.protocol == key else False) for key in self.keys]
            super().__init__(custom_id=custom_id, placeholder=placeholder, min_values=min_values, max_values=max_values, options=options, disabled=disabled, row=row)

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            if self.values[0] in list(self.keys):
                await updurl_menu(self.per_view.ctx, self.per_view.url, self.values[0])
                await lib.valide_intaraction(interaction)

    class Valide_button(discord.ui.Button):
        def __init__(self, *, view, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.comfyui_domain = view.url
            self._protocol = view._protocol

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await updurl(interaction, self.comfyui_domain, self._protocol)

class Config_view(discord.ui.View):
    def __init__(self, *, ctx: discord.Interaction, timeout: lib.Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.ctx=ctx

    @discord.ui.button(label="Edit URL",style=discord.ButtonStyle.gray)
    async def updurl_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await updurl_menu(self.ctx)
        await lib.valide_intaraction(interaction)

#############################################################
#                          Modal                           #
#############################################################

class Updurl_modal(discord.ui.Modal):
    def __init__(self, *, view: Updurl_view, title: str = lib.MISSING, timeout: lib.Optional[float] = None, custom_id: str = lib.MISSING) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.url = discord.ui.TextInput(label="url", placeholder="localhost:8188")
        self.add_item(self.url)
        self.per_view = view

    async def on_submit(self, interaction: discord.Interaction) -> None:
        val = self.url.__str__()
        if not val:
            raise Exception()
        else:
            await updurl_menu(self.per_view.ctx, self.url.__str__(), self.per_view._protocol)
            await lib.valide_intaraction(interaction)


#############################################################
#                          Config                           #
#############################################################
async def updurl_menu(ctx: discord.Interaction, url="", _class=""):
    embed=discord.Embed(title=":gear:  ComfyUI Config")
    embed.description = "Update ComfyUI url"
    prot = _class
    print(prot)
    await ctx.edit_original_response(embed=embed, view=Updurl_view(ctx=ctx, url=url, _protocol=prot))

@Lib.app.config()
async def config_menu(ctx: discord.Interaction):
    if not ctx.response.is_done():
        await ctx.response.send_message(embed=discord.Embed(title="Chargement..."), ephemeral=True)
    embed=discord.Embed(title=":gear:  ComfyUI Config")
    embed.add_field(name="Info :", value=f"ComfyUI URL : {protocol}://{domain}")
    embed.add_field(name="Info :", value=f"Workflow loaded : {1}")
    embed.add_field(name="Info :", value=f"Model loaded : {len(models)}")
    await ctx.edit_original_response(embed=embed, view=Config_view(ctx=ctx))