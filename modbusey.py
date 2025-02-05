from pymodbus.client import ModbusTcpClient
import readline
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def main():
    print("___  ___            _ ______")
    print("|  \\/  |           | || ___ \\")
    print("| .  . |  ___    __| || |_/ / _   _  ___   ___  _   _ ")
    print("| |\\/| | / _ \\  / _` || ___ \\| | | |/ __| / _ \\| | | |")
    print("| |  | || (_) || (_| || |_/ /| |_| |\\__ \\|  __/| |_| |")
    print("\\_|  |_/ \\___/  \\__,_|\\____/  \\__,_||___/ \\___| \\__, |")
    print("                                                 __/ |")
    print("                                                |___/ ")

    print(Fore.RED + "\nModbus Cheat Sheet:" + Style.RESET_ALL)
    print(Fore.BLUE + "Coil: " + Style.RESET_ALL + "writable boolean")
    print(Fore.BLUE + "Discrete Input: " + Style.RESET_ALL + "read-only boolean")
    print(Fore.BLUE + "Holding Register: " + Style.RESET_ALL + "writable 16-bit register")
    print(Fore.BLUE + "Input Register: " + Style.RESET_ALL + "read-only 16-bit register")

    plc_ip = input("\nEnter PLC IP: ").strip()
    client = ModbusTcpClient(plc_ip)
    if not client.connect():
        print(f"Failed to connect to PLC at {plc_ip}")
        quit()
    else:
        print(f"Connected to PLC at {plc_ip}")

    while True:
        print("\nSelect a function:")
        print("1. Read Coils")
        print("2. Read Discrete Inputs")
        print("3. Read Holding Registers")
        print("4. Read Input Registers")
        print("5. Write Coil")
        print("6. Write Contiguous Coils")
        print("7. Write Holding Register")
        print("8. Mask Write Holding Register")

        choice = input("\nEnter choice: ").strip()

        # Read Coils
        if choice == "1":
            print(              "\n*************")
            print(Fore.YELLOW + "Reading Coils" + Style.RESET_ALL)
            print(              "*************")
            try:
                start = int(input("\nStarting address: ").strip())
                count = int(input("Count to read: ").strip())
            except ValueError:
                print("Invalid input")
                continue

            print("\n")

            responses = []
            for address in range (start, start + count):
                response = client.read_coils(address)
                coil_value = response.bits[0]
                responses.append(coil_value)
            for value in responses:
                color = GREEN if value else RED
                print(f"Address {start:3d}: {color}{value}{RESET}")
                start += 1

        # Read Discrete Inputs
        if choice == "2":
            print(              "\n***********************")
            print(Fore.YELLOW + "Reading Discrete Inputs" + Style.RESET_ALL)
            print(              "***********************")
            try:
                start = int(input("\nStarting address: ").strip())
                count = int(input("Count to read: ").strip())
            except ValueError:
                print("Invalid input")
                continue

            print("\n")

            responses = []
            for address in range(start, start + count):
                response = client.read_discrete_inputs(address)
                input_value = response.bits[0]
                responses.append(input_value)
            for value in responses:
                color = GREEN if value else RED
                print(f"Address {start:3d}: {color}{value}{RESET}")
                start += 1

        # Read Holding Registers
        if choice == "3":
            print(              "\n*************************")
            print(Fore.YELLOW + "Reading Holding Registers" + Style.RESET_ALL)
            print(              "*************************")
            try:
                start = int(input("\nStarting address: ").strip())
                count = int(input("Count to read: ").strip())
            except ValueError:
                print("Invalid input")
                continue

            print("\n")

            responses = []
            for address in range(start, start + count):
                response = client.read_holding_registers(address)
                register_value = response.registers
                responses.append(register_value)
            for value in responses:
                color = RED if value[0] == 0 else GREEN
                print(f"Address {start:3d}: {color}{value}{RESET}")
                start += 1

        # Read Input Registers
        if choice == "4":
            print(              "\n***********************")
            print(Fore.YELLOW + "Reading Input Registers" + Style.RESET_ALL)
            print(              "***********************")
            try:
                start = int(input("\nStarting address: ").strip())
                count = int(input("Count to read: ").strip())
            except ValueError:
                print("Invalid input")
                continue

            print("\n")

            responses = []
            for address in range(start, start + count):
                response = client.read_input_registers(address)
                register_value = response.registers
                responses.append(register_value)
            for value in responses:
                color = RED if value[0] == 0 else GREEN
                print(f"Address {start:3d}: {color}{value}{RESET}")
                start += 1

        # Write Coil
        if choice == "5":
            print(              "\n************")
            print(Fore.YELLOW + "Writing Coil" + Style.RESET_ALL)
            print(              "************")
            try:
                coil_address = int(input("\nCoil address: ").strip())
                response = client.read_coils(coil_address)
                coil_value = response.bits[0]
                color = GREEN if coil_value else RED
                print(f"Current Coil Value: {color}{coil_value}{RESET}")
                new_coil_value = int(input("Desired Coil Value (0/1): ").strip())
            except ValueError:
                print("Invalid input")
                continue

            print("\n")

            response = client.write_coil(coil_address, new_coil_value)
            print("\nResponse: ", response)
            response = client.read_coils(coil_address)
            coil_value = response.bits[0]
            color = GREEN if coil_value else RED
            print(f"\nNew Coil Value: {color}{coil_value}{RESET}")

        # Write Contiguous Coils
        if choice == "6":
            print(              "\n************************")
            print(Fore.YELLOW + "Writing Contiguous Coils" + Style.RESET_ALL)
            print(              "************************")
            try:
                start = int(input("\nStarting address: ").strip())
                count = int(input("Count to write: ").strip())
            except ValueError:
                print("Invalid input")
                continue

            index = start
            print("\n")
            print("Current Coil Values:")

            responses = []

            for address in range (start, start + count):
                response = client.read_coils(address)
                coil_value = response.bits[0]
                responses.append(coil_value)

            for value in responses:
                color = GREEN if value else RED
                print(f"Address {index:3d}: {color}{value}{RESET}")
                index += 1

            new_coil_value = int(input("\nDesired Value (0/1): ").strip())
            coil_values = [new_coil_value] * count

            response = client.write_coils(start, coil_values)
            print("\nResponse: ", response)

            index = start
            print("\n")
            print("New Coil Values:")

            responses = []

            for address in range (start, start + count):
                response = client.read_coils(address)
                coil_value = response.bits[0]
                responses.append(coil_value)

            for value in responses:
                color = GREEN if value else RED
                print(f"Address {index:3d}: {color}{value}{RESET}")
                index += 1

        # Write Holding Register
        if choice == "7":
            print(              "\n************************")
            print(Fore.YELLOW + "Writing Holding Register" + Style.RESET_ALL)
            print(              "************************")

            try:
                register_address = int(input("\nRegister address: ").strip())
                response = client.read_holding_registers(register_address)
                register_value = response.registers
                print(f"Current Register Value: {register_value}")
                new_register_value = int(input("Desired Register Value: ").strip())
            except ValueError:
                print("Invalid input")
                continue

            print("\n")

            response = client.write_register(register_address, new_register_value)
            print("\nResponse: ", response)
            response = client.read_holding_registers(register_address)
            register_value = response.registers
            print(f"\nNew Register Value: {register_value}")

        if choice == "8":
            print(              "\n*****************************")
            print(Fore.YELLOW + "Mask Writing Holding Register" + Style.RESET_ALL)
            print(              "*****************************")

            try:
                register_address = int(input("\nRegister address: ").strip())
            except ValueError:
                print("Invalid input")
                continue

            read_response = client.read_holding_registers(register_address)
            old_value = read_response.registers[0]

            print(f"Current Register Value: {old_value}")

            try:
                desired_value = int(input("Desired Register Value: ").strip())
                if not (0 <= desired_value <= 0xFFFF):
                    raise ValueError
            except ValueError:
                print("Invalid value. Must be an integer between 0 and 65535")

            and_mask = 0xFFFF
            or_mask = 0x0000

            for bit in range(16):
                bit_mask = 1 << bit
                old_bit = (old_value >> bit) & 1
                new_bit = (desired_value >> bit) & 1

                if old_bit == 1 and new_bit == 0:
                    and_mask &= ~bit_mask
                elif old_bit == 0 and new_bit == 1:
                    or_mask |= bit_mask

            write_response = client.mask_write_register(address=register_address, and_mask=and_mask, or_mask=or_mask)

            print("\nResponse: ", write_response)

            read_response = client.read_holding_registers(register_address)
            print(f"New Register Value: {read_response.registers[0]}")



if __name__ == '__main__':
    main()
