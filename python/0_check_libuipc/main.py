import threading
import time
import asyncio

from asset_dir import AssetDir

import uipc
from uipc import (Engine, Logger, 
                  unit, builtin, dev,
                  ResidentThread)

if __name__ == '__main__':
    print(f'pyuipc version: {uipc.__version__}')
    print(f'asset_path: {AssetDir.asset_path()}')
    print(f'tetmesh_path: {AssetDir.tetmesh_path()}')
    print(f'trimesh_path: {AssetDir.trimesh_path()}')
    print(f'this file output_path: {AssetDir.output_path(__file__)}')
    print()
    
    print('* UIPC INFO:')
    print('-'*80)
    print('constitutions:')
    print(dev.ConstitutionUIDInfo())
    print('-'*80)
    print('implicit_geomeries:')
    print(dev.ImplicitGeometryUIDInfo())
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

    def init_engine():
        engine = Engine('cuda', workspace=AssetDir.output_path(__file__))
        time.sleep(0.5) # Just make some delay
        print(f'Engine initialized: {engine}')

    start_time = time.time()
    symbols = ['|', '/', '-', '\\']
    i = 0

    rt = ResidentThread()

    rt.post(init_engine)
    while not rt.is_ready():
        print('Waiting for cuda engine to initialize. ', end='')
        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f'Elapsed time: {elapsed_time:.2f} seconds', end='')
        print(f' {symbols[i % len(symbols)]}', end='\r')
        i += 1
        time.sleep(0.05)