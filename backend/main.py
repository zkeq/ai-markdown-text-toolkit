import json
import time

import aiohttp
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from pypinyin import pinyin, lazy_pinyin, Style

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def write_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


class Gpt:
    api_config = ""
    key = ""
    prefix = ""
    model = ""

    def __init__(self):
        config = read_config()
        self.api_config = config["api_config"]
        self.key = config["key"]
        self.prefix = config["prefix"]
        self.model = config["model"]


UseGpt = Gpt()


class GetConfigItem(BaseModel):
    password: str


@app.post("/info")
def get_info(item: GetConfigItem):
    if item.password != os.getenv("PASSWORD"):
        return {
            "msg": "密码错误, 请重试"
        }
    return {
        "key": UseGpt.key,
        "api_config": UseGpt.api_config,
        "prefix": UseGpt.prefix,
        "model": UseGpt.model
    }


class PutConfigItem(BaseModel):
    password: str
    key: str
    api_config: str
    prefix: str
    model: str


@app.put("/info")
def get_info(item: PutConfigItem):
    if item.password != os.getenv("PASSWORD"):
        return {
            "msg": "密码错误, 请重试"
        }
    UseGpt.key = item.key
    UseGpt.api_config = item.api_config
    UseGpt.prefix = item.prefix
    UseGpt.model = item.model
    write_config({
        "key": item.key,
        "api_config": item.api_config,
        "prefix": item.prefix,
        "model": item.model
    })
    return {
        "key": UseGpt.key,
        "api_config": UseGpt.api_config,
        "prefix": UseGpt.prefix,
        "model": UseGpt.model
    }


def check_timestamp(timestamp):
    current_time = int(time.time())
    # 设定时间窗口为60秒
    if current_time - timestamp > 60:
        return False
    return True


class QuestionItem(BaseModel):
    timestamp: int
    text: str
    prefix: Optional[str] = UseGpt.prefix


def verify_referer(referer: str = Header(None)):
    allowed_referer = os.getenv("ALLOWED_REFERER")
    if referer != allowed_referer:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid referer")
    

@app.post("/improve")
async def improve(item: QuestionItem, referer: str = Header(None)):
    verify_referer(referer)
    if not check_timestamp(item.timestamp):
        return {"error": "时间戳验证失败"}

    async def event_stream(_question, prefix):
        prefix = UseGpt.prefix if not prefix else prefix
        async with aiohttp.ClientSession() as session:
            session.headers.update({
                "Authorization": "Bearer " + UseGpt.key,
            })
            async with session.post(f"{UseGpt.api_config}/v1/chat/completions",
                                    json={
                                        'model': UseGpt.model,
                                        'messages': [
                                            {'role': 'system', 'content': prefix},
                                            {'role': 'user', 'content': _question}
                                        ],
                                        'stream': True
                                    }
                    , ssl=False
                                    ) as response:
                async for chunk in response.content.iter_chunked(1):
                    yield chunk

    # Return events to client as a stream
    return StreamingResponse(event_stream(item.text, item.prefix), media_type="text/event-stream")


class PinyinItem(BaseModel):
    timestamp: int
    text: str
    type: str


@app.post("/pinyin")
async def root(item: PinyinItem, referer: str = Header(None)):
    verify_referer(referer)
    item = item.dict()
    if not check_timestamp(item["timestamp"]):
        return {"error": "密钥验证失败"}
    if item["type"] == "intonation":
        pinyin_text = pinyin(item["text"])
        # 使用列表推导式将二维数组转换为一维数组
        pinyin_text_flat = [item for sublist in pinyin_text for item in sublist]
        # 将一维数组转换为以空格分割的字符串
        pinyin_text_str = ' '.join(pinyin_text_flat)
        return {
            "text": pinyin_text_str
        }
    if item["type"] == "noIntonation":
        return {
            "text": ' '.join(lazy_pinyin(item["text"]))
        }
    if item["type"] == "numberIntonation":
        pinyin_text = pinyin(item["text"], style=Style.TONE3)
        # 使用列表推导式将二维数组转换为一维数组
        pinyin_text_flat = [item for sublist in pinyin_text for item in sublist]
        # 将一维数组转换为以空格分割的字符串
        pinyin_text_str = ' '.join(pinyin_text_flat)
        return {
            "text": pinyin_text_str
        }
    if item["type"] == "alphabet":
        return {
            "text": ' '.join(lazy_pinyin(item["text"], style=Style.FIRST_LETTER))
        }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8006, proxy_headers=True, forwarded_allow_ips="*")
