import os
import asyncio
from pathlib import Path
from singleton_decorator import SingletonDecorator
from retry import retry  # Import the retry decorator here

@SingletonDecorator
class MyConnection:
    """
    This class represents a connection object and provides methods for connecting to a client.
    """

    def __init__(self, client_instance):
        self.client = client_instance

    @retry(TimeoutError, tries=11, delay=8, backoff=3)  # Adjust parameters as needed
    async def connect(self, attempts=8):
        check, reason = await self.client.connect()
        if not check:
            attempt = 0
            while attempt <= attempts:
                if not self.client.check_connect():
                    check, reason = await self.client.connect()
                    if check:
                        print("Reconectado com sucesso!!!")
                        break
                    print("Erro ao reconectar.")
                    attempt += 1
                    if Path(os.path.join(".", "session.json")).is_file():
                        Path(os.path.join(".", "session.json")).unlink()
                    print(f"Tentando reconectar, tentativa {attempt} de {attempts}")
                elif not check:
                    attempt += 1
                else:
                    break
                await asyncio.sleep(5)
            return check, reason
        return check, reason

    def close(self):
        """
        Closes the client connection.
        """
        self.client.close()


# import os
# import asyncio
# from pathlib import Path
# from singleton_decorator import SingletonDecorator


# @SingletonDecorator
# class MyConnection:
#     """
#     This class represents a connection object and provides methods for connecting to a client.
#     """

#     def __init__(self, client_instance):
#         self.client = client_instance

#     async def connect(self, attempts=5):
#         check, reason = await self.client.connect()
#         if not check:
#             attempt = 0
#             while attempt <= attempts:
#                 if not self.client.check_connect():
#                     check, reason = await self.client.connect()
#                     if check:
#                         print("Reconectado com sucesso!!!")
#                         break
#                     print("Erro ao reconectar.")
#                     attempt += 1
#                     if Path(os.path.join(".", "session.json")).is_file():
#                         Path(os.path.join(".", "session.json")).unlink()
#                     print(f"Tentando reconectar, tentativa {attempt} de {attempts}")
#                 elif not check:
#                     attempt += 1
#                 else:
#                     break
#                 await asyncio.sleep(5)
#             return check, reason
#         return check, reason

#     def close(self):
#         """
#         Closes the client connection.
#         """
#         self.client.close()