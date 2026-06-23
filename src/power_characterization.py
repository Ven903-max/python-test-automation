# Power characterization test
import time
import csv
from datetime import datetime

import pyvisa

from instrument_drivers import SCPIInstrument


SUPPLY_ADDRESS = "TCPIP::SUPPLY_IP::INSTR"
LOAD_ADDRESS = "TCPIP::LOAD_IP::INSTR"

INPUT_VOLTAGE = 12.0
CURRENT_SWEEP = [0.1, 0.25, 0.5, 0.75, 1.0]


def calculate_efficiency(pin, pout):
    if pin <= 0:
        return 0
    return (pout / pin) * 100


def main():

    rm = pyvisa.ResourceManager()

    supply = SCPIInstrument(rm, SUPPLY_ADDRESS)
    load = SCPIInstrument(rm, LOAD_ADDRESS)

    filename = (
        f"efficiency_results_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    try:

        supply.write(f"VOLT {INPUT_VOLTAGE}")
        supply.write("OUTP ON")

        with open(filename, "w", newline="") as csv_file:

            writer = csv.writer(csv_file)

            writer.writerow(
                [
                    "Load Current (A)",
                    "Input Power (W)",
                    "Output Power (W)",
                    "Efficiency (%)"
                ]
            )

            for current in CURRENT_SWEEP:

                load.write(f":CURR {current}")
                load.write(":INP ON")

                time.sleep(1)

                vin = float(supply.query("MEAS:VOLT?"))
                iin = float(supply.query("MEAS:CURR?"))

                vout = float(load.query("MEAS:VOLT?"))
                iout = float(load.query("MEAS:CURR?"))

                pin = vin * iin
                pout = vout * iout

                efficiency = calculate_efficiency(pin, pout)

                writer.writerow(
                    [
                        current,
                        round(pin, 3),
                        round(pout, 3),
                        round(efficiency, 2),
                    ]
                )

                print(
                    f"Current={current:.2f}A | "
                    f"Efficiency={efficiency:.2f}%"
                )

    finally:

        load.write(":INP OFF")
        supply.write("OUTP OFF")

        load.close()
        supply.close()

        rm.close()


if __name__ == "__main__":
    main()
