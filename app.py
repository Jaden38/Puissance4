import asyncio
import websockets
import signal
import json
from connect4 import PLAYER1, PLAYER2, Connect4


async def handler(websocket):
    game = Connect4()  # On instancie la classe Connect4
    redTurn = True  # C'est le rouge qui commence
    try:
        # Lecture du message envoyé par le navigateur
        async for message in websocket:
            # A chaque tour on change de joueur
            player = PLAYER1 if redTurn else PLAYER2
            redTurn = not redTurn
            event = json.loads(message)

            assert event["type"] == "play"
            column = event["column"]
            try:
                # On joue le coup reçu
                row = game.play(player, column)
            except RuntimeError as exc:
                # On a reçu un evenement "error" pour coup illégal
                event = {
                    "type": "error",
                    "message": str(exc),
                }
                await websocket.send(json.dumps(event))
                continue
            # On forge un evenement "play" pour afficher sur le navigateur
            event = {
                "type": "play",
                "player": player,
                "column": column,
                "row": row,
            }
            await websocket.send(json.dumps(event))
            # Si ce dernier coup est gagnant : On envoie un evenement "win"
            if game.winner is not None:
                event = {
                    "type": "win",
                    "player": game.winner,
                }
                await websocket.send(json.dumps(event))

    except websockets.ConnectionClosedOK:
        print("Connection closed normally.")
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except ConnectionResetError:
        print("Connection was reset unexpectedly by the remote host.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Handler routine ended.")


async def main():
    stop = asyncio.Future()

    def stop_handler(signum, frame):
        stop.set_result(None)
    signal.signal(signal.SIGINT, stop_handler)

    async with websockets.serve(handler, "localhost", 8001):
        print("Server started at ws://localhost:8001")
        await stop  # wait until a stop signal is received

    print("Server shutting down.")

if __name__ == "__main__":
    asyncio.run(main())
