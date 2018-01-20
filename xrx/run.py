import asyncio
import logging

from .events import xboxdrv_event_stream
from .stream import x_stream

from rx.concurrency import AsyncIOScheduler

scheduler = AsyncIOScheduler()


logging.basicConfig(level=logging.INFO)


ev_stream = ['a', 'b', 'c']


stream = x_stream(ev_stream).subscribe_on(scheduler)

loop = asyncio.get_event_loop()
loop.run_forever()
