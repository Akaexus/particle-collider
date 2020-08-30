from modules.config import Config
from modules.simulation.engine import Engine
import copy
import os
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

class Benchmark:
    def __init__(self, cnf):
        self.config = cnf
        folder_name = datetime.now().strftime('benchmark_%Y-%m-%d_%H:%M:%S')
        self.path = f'{self.config["path"]}/{folder_name}'
        os.mkdir(self.path)

    def run(self):
        if 'test1' in self.config['benchmark']:
            self.test1()
        if 'test2' in self.config['benchmark']:
            self.test2()

    def runWithConfig(self, cnf):
        config = Config(cnf)
        engine = Engine(config)
        while engine.ticks_left > 0:
            engine.tick()
            engine.ticks_left -= 1
        return engine.detector.getPressure()

    def test1(self):
        os.mkdir(f'{self.path}/test1')
        base_config = self.config['simulation']
        test_config = self.config['benchmark']['test1']
        for atom_quantity in test_config['params']['atoms']['number']:
            position = test_config['params']['detector']['position']
            detector_position = position['start']

            pressures = []
            positions = []

            while detector_position <= position['stop']:
                print('Test1 - atomów {}, pozycja {}'.format(atom_quantity, detector_position))
                cnf = copy.deepcopy(base_config)
                cnf['atoms']['number'] = int(atom_quantity)
                cnf['detector']['position'] = detector_position
                # symulacja
                pressure = self.runWithConfig(cnf)
                pressures.append(pressure)
                positions.append(detector_position)
                detector_position += position['step']
            plt.plot(positions, pressures)
            plt.xlabel('Pozycja detektora [H]')
            plt.ylabel('Ciśnienie liniowe P(H)')
            plt.title('Zależność ciśnienia liniowego od pozycji detektora dla {} atomów'.format(atom_quantity))
            plt.savefig(
                f'{self.path}/test1/graph_n{atom_quantity}.png',
                dpi=300
            )
            plt.clf()

    def test2(self):
        os.mkdir(f'{self.path}/test2')
        base_config = self.config['simulation']
        test_config = self.config['benchmark']['test2']
        for detector_position in test_config['params']['detector']['position']:
            atoms_range = test_config['params']['atoms']['number']
            atom_quantity = atoms_range['start']

            pressures = []
            atoms_number = []

            while atom_quantity <= atoms_range['stop']:
                print('Test2 - atomów {}, pozycja {}'.format(atom_quantity, detector_position))
                cnf = copy.deepcopy(base_config)
                cnf['atoms']['number'] = int(atom_quantity)
                cnf['detector']['position'] = detector_position
                # symulacja
                pressure = self.runWithConfig(cnf)
                pressures.append(pressure)
                atoms_number.append(atom_quantity)
                atom_quantity += atoms_range['step']
            plt.plot(atoms_number, pressures)
            plt.xlabel('Ilość atomów (N)')
            plt.ylabel('Ciśnienie liniowe P(N)')
            plt.title('Zależność ciśnienia liniowego od ilości atomów dla pozycji detektora = {}'.format(detector_position))
            plt.savefig(
                f'{self.path}/test2/graph_h{detector_position}.png',
                dpi=300
            )
            plt.clf()