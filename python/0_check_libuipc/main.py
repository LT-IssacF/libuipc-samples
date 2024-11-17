import threading
import time

from pyuipc_loader import pyuipc
from pyuipc import Engine, Logger
from asset_dir import AssetDir

finish = False
def waiting():
    symbols = ['|', '/', '-', '\\']
    i = 0
    while(True):
        if(finish):
            break
        print('Waiting for cuda engine to initialize. ', end='')
        print(f' {symbols[i % len(symbols)]}', end='\r')
        i+=1
        time.sleep(0.25)
        pass

if __name__ == '__main__':
    print(f'pyuipc version: {pyuipc.__version__}')
    print(f'asset_path: {AssetDir.asset_path()}')
    print(f'tetmesh_path: {AssetDir.tetmesh_path()}')
    print(f'trimesh_path: {AssetDir.trimesh_path()}')
    print(f'this file output_path: {AssetDir.output_path(__file__)}')
    
    Logger.set_level(Logger.Info)
    
    print('''
* The first time to initialize the engine will take a while
  because the cuda kernels need to be compiled.
''')

    t = threading.Thread(target=waiting)
    t.start()
    
    engine = Engine('cuda', AssetDir.output_path(__file__))
    
    finish = True
    t.join()

