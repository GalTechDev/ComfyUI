import discord
import requests
from understar.system import lib
from typing import List
import websocket
import requests
import json
from threading import Thread
from uuid import uuid4
from random import randint
import asyncio
from io import BytesIO

Lib = lib.App()

domain = '127.0.0.1:8188'
save_path = ("sd_output", "output.png")
tasks = []
queue_remaining = 0
models = []

#############################################################
#                       Workflow                            #
#############################################################

workflow = {
    "client_id": "23d654ab337f48d9bbad8559f3ed7407",
    "prompt": {
        "42": {
            "inputs": {
                "ckpt_name": "dreamshaperXL_v21TurboDPMSDE.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "44": {
            "inputs": {
                "seed": 879523854994921,
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
                "width": 512,
                "height": 512,
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
                            "dreamshaperXL_v21TurboDPMSDE.safetensors"
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
                            512,
                            512,
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

#############################################################
#                     Other Class                           #
#############################################################

class Task:
    def __init__(self, ctx: discord.Interaction, uuid: str, positive: str, negative: str) -> None:
        self.ctx = ctx
        self.uuid = uuid
        self.positive = positive
        self.negative = negative
        self.thread = None

        send_prompt(self.uuid, self.positive, self.negative)


    async def wait4img(self):
        while True:
            response = requests.get(f"http://{domain}/view?filename={self.uuid}_00001_.png&type=output")
            if response.status_code == 200:
                image = BytesIO(response.content)                
                break
            await asyncio.sleep(1)
        file=discord.File(fp=image, filename='image.png')
        await self.ctx.edit_original_response(content=f"Positive : **{self.positive}**\nNegative : **{self.negative}**", attachments=[file])
        if tasks:
            tasks.pop(0)
        await update_task()

    async def update_msg(self):
        if tasks[0] == self:
            if not self.thread:
                await self.ctx.edit_original_response(content=f"Generating...\nPositive : **{self.positive}**\nNegative : **{self.negative}**")
                asyncio.create_task(self.wait4img())

        else:
            await self.ctx.edit_original_response(content=f"Queue remaining : {queue_remaining}\nPositive : **{self.positive}**\nNegative : **{self.negative}**")

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
            choices.append(discord.app_commands.Choice(name=m, value=m))
        return choices[:25]

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
        await interaction.response.send_message(f'Queue remaining : {queue_remaining}\nPositive : **{self.positive.value}**\nNegative : **{self.negative.value}**', ephemeral=False)
        tasks.append(Task(interaction, str(uuid4()), self.positive.value, self.negative.value))
        await update_task()
        
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Une erreur est survenu', ephemeral=True)

#############################################################
#                           ComfyUI                         #
#############################################################

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

def send_prompt(uuid: str, positive_prompt: str = "", negative_prompt: str = ""):
    prompt_url = f"http://{domain}/prompt"

    wrk = workflow.copy()
    wrk["prompt"]["44"]["inputs"]["seed"] = randint(100000000000000,999999999999999)
    wrk["prompt"]["48"]["inputs"]["text"] = positive_prompt
    wrk["prompt"]["51"]["inputs"]["text"] = negative_prompt
    wrk["prompt"]["54"]["inputs"]["filename_prefix"] = uuid

    wrk = json.dumps(wrk).encode('utf-8')

    r = requests.post(prompt_url, data=wrk, headers={'Content-Type': 'application/json'})

async def update_task():
    for task in tasks:
        await task.update_msg()

#############################################################
#                           Event                           #
#############################################################

@Lib.event.event()
async def on_ready():
    global models
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