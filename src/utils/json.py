import orjson


async def load(fp) -> dict:
    return orjson.loads(await fp.read())


async def dump(fp, content: dict) -> None:
    await fp.write(orjson.dumps(content))
