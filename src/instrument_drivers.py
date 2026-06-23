# Instrument driver abstraction layer
import pyvisa


class SCPIInstrument:
    def __init__(self, resource_manager, resource_string):
        self.instrument = resource_manager.open_resource(resource_string)

    def write(self, command):
        self.instrument.write(command)

    def query(self, command):
        return self.instrument.query(command)

    def close(self):
        self.instrument.close()
