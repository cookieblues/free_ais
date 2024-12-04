import os
import asyncio
import json
from datetime import datetime, timezone

import websockets
from dotenv import load_dotenv

load_dotenv()


async def connect_ais_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {
            "APIKey": os.environ["aisstreamio"],  # Required!
            "BoundingBoxes": [[[-90, -180], [90, 180]]],  # Required!
            "FiltersShipMMSI": ["368207620", "367719770", "211476060"],  # Optional!
            "FilterMessageTypes": ["PositionReport"],  # Optional!
        }

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                # the message parameter contains a key of the message type which contains the message itself
                ais_message = message["Message"]["PositionReport"]
                print(
                    f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Latitude: {ais_message['Longitude']}"
                )


if __name__ == "__main__":
    asyncio.run(asyncio.run(connect_ais_stream()))
