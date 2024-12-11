# Needed imports
import json
import socket
import inspect
from threading import Thread

# Define buffer size constant
SIZE = 1024  # You can adjust this value based on your needs

# rpc.py
class RPCServer:
    def __init__(self, host:str='127.0.0.1', port:int=8000) -> None:
        self.host = host
        self.port = port
        self.address = (host, port)
        self._methods = {}

    # Within RPCServer
    def registerMethod(self, function) -> None:
        try:
            self._methods.update({function.__name__ : function})
        except:
            raise Exception('A non function object has been passed into RPCServer.registerMethod(self, function)')

    # Within RPCServer  
    def registerInstance(self, instance=None) -> None:
        try:
            # Regestring the instance's methods
            for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
                if not functionName.startswith('__'):
                    self._methods.update({functionName: function})
        except:
            raise Exception('A non class object has been passed into RPCServer.registerInstance(self, instance)')

    def __handle__(self, client:socket.socket, address:tuple) -> None:
        print(f'Managing requests from {address}.')
        while True:
            try:
                functionName, args, kwargs = json.loads(client.recv(SIZE).decode())
            except: 
                print(f'! Client {address} disconnected.')
                break
            # Showing request Type
            print(f'> {address} : {functionName}({args})')

            try:
                response = self._methods[functionName](*args, **kwargs)
            except Exception as e:
                # Send back exeption if function called by client is not registred 
                client.sendall(json.dumps(str(e)).encode())
            else:
                client.sendall(json.dumps(response).encode())

        print(f'Completed requests from {address}.')
        client.close()
    
        # within RPCServer
    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()

            print(f'+ Server {self.address} running')
            while True:
                try:
                    client, address = sock.accept()

                    Thread(target=self.__handle__, args=[client, address]).start()

                except KeyboardInterrupt:
                    print(f'- Server {self.address} interrupted')
                    break;

class RPCClient:
    def __init__(self, host:str='localhost', port:int=8000) -> None:
        self.__sock = None
        self.__address = (host, port)
    # Within RPCClient
    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Attempting to connect to {self.__address}...")  # Add connection logging
            self.__sock.connect(self.__address)
            print("Successfully connected to server")  # Confirm successful connection
            return self
        except ConnectionRefusedError:
            print(f"Connection refused - Is the server running at {self.__address}?")
            raise Exception('Server is not running or refusing connections.')
        except socket.error as e:
            print(f"Socket error occurred: {e}")
            raise Exception(f'Client was not able to connect: {str(e)}')
        except Exception as e:
            print(f"Unexpected error during connection: {e}")
            raise Exception(f'Client was not able to connect: {str(e)}')
    
    def disconnect(self):
        try:
            self.__sock.close()
        except:
            pass
    
        # Within RPCClient
    def __getattr__(self, __name: str):
        def excecute(*args, **kwargs):
            max_retries = 10  # Add retry limit
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())
                    response = json.loads(self.__sock.recv(SIZE).decode())
                    return response
                except ConnectionResetError:
                    retry_count += 1
                    print(f"Connection was reset by the server. Attempt {retry_count} of {max_retries}...")
                    self.disconnect()  # Clean up existing socket
                    try:
                        self.connect()  # Try to reconnect
                    except Exception as e:
                        if retry_count == max_retries:
                            raise Exception(f"Failed to reconnect after {max_retries} attempts: {str(e)}")
                        continue
                except Exception as e:
                    self.disconnect()  # Clean up the socket
                    raise Exception(f"RPC call failed: {str(e)}")
        return excecute