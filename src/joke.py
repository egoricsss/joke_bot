from utils import http_request, JokeDTM
import json

__all__ = ["get_joke"]


async def get_joke() -> JokeDTM:
    joke = await http_request(
        "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart"
    )
    jokeDTM = JokeDTM.model_validate(json.loads(joke))
    return jokeDTM
