from MapService import MapService
from rpyc.utils.server import ThreadedServer


if __name__ == "__main__":
    try:
        print("[!] RPC server is up.")
        server = ThreadedServer(MapService, port=18861, protocol_config={
            'allow_public_attrs': True,
            'allow_setattr': True,
            'allow_pickle': True
        })
        server.start()
    except Exception as e:
        print(e)
        print("[!] Exiting RPC server.")
