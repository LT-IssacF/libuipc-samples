import threading
import time
from uipc import Engine, Logger
from asset_dir import AssetDir
from multiprocessing import Process, Queue

from uipc import builtin
from uipc import unit

def print_sorted(uids):
    uids = sorted(uids, key=lambda x: x['uid'])
    for u in uids:
        uid = u['uid']
        name = u['name']
        type = u['type']
        print(f'uid: {uid}, name: {name}, type: {type}')

def waiting(q : Queue):
    symbols = ['|', '/', '-', '\\']
    i = 0
    start_time = time.time()
    elapsed_time = 0
    while(True):
        if(not q.empty()):
            break
        print('Waiting for cuda engine to initialize. ', end='')
        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f'Elapsed time: {elapsed_time:.2f} seconds', end='')
        print(f' {symbols[i % len(symbols)]}', end='\r')
        i+=1
        time.sleep(0.05)
        pass

if __name__ == '__main__':
    print(f'uipc version: {uipc.__version__}')
    print(f'asset_path: {AssetDir.asset_path()}')
    print(f'tetmesh_path: {AssetDir.tetmesh_path()}')
    print(f'trimesh_path: {AssetDir.trimesh_path()}')
    print(f'this file output_path: {AssetDir.output_path(__file__)}')

    print()
    
    constitutions = builtin.ConstitutionUIDCollection.instance().to_json()
    implicit_geomeries = builtin.ImplicitGeometryUIDCollection.instance().to_json()
    
    print('* UIPC INFO:')
    print('-'*80)
    print('constitutions:')
    print_sorted(constitutions)
    print('-'*80)
    print('implicit_geomeries:')
    print_sorted(implicit_geomeries)
    print('-'*80)
    print('units:')
    print(f's={unit.s}')
    print(f'm={unit.m}')
    print(f'mm={unit.mm}')
    print(f'km={unit.km}')
    print(f'Pa={unit.Pa}')
    print(f'kPa={unit.kPa}')
    print(f'MPa={unit.MPa}')
    print(f'GPa={unit.GPa}')

    Logger.set_level(Logger.Warn)
    
    print('''
* The first time to initialize the engine will take a while (maybe several minutes)
  because the cuda kernels need to be compiled.
''')
    # create a process to wait for the engine to initialize
    Q = Queue()
    p = Process(target=waiting, args=(Q,))
    p.start()

    engine = Engine('cuda', AssetDir.output_path(__file__))
    
    # signal the waiting process to stop
    Q.put(1)
    p.join()
    print(' ' * 100, end='\r')
    print('* Engine initialized.')

