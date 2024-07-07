import mido
import threading
import sys

# Conversion function from hex to decimal
def hex_to_decimal(hex_list):
    return [int(value, 16) for value in hex_list]

# Replace with your actual SysEx messages in hexadecimal
SYSEX_MESSAGE_1_HEX = [0x21, 0x25, 0x7F, 0x4D, 0x50, 0x2D, 0x64, 0x12, 0x10, 0x01, 0x00, 0x01, 0x00, 0x26]
SYSEX_MESSAGE_2_HEX = [0x21, 0x25, 0x7F, 0x4D, 0x50, 0x2D, 0x64, 0x12, 0x10, 0x02, 0x00, 0x02, 0x00, 0x37, 0x03, 0x00, 0x01]

# Convert them to decimal
SYSEX_MESSAGE_1 = hex_to_decimal([hex(value) for value in SYSEX_MESSAGE_1_HEX])
SYSEX_MESSAGE_2 = hex_to_decimal([hex(value) for value in SYSEX_MESSAGE_2_HEX])

# Adjust virtual MIDI port name based on platform
if sys.platform == 'win32':
    virtual_port_name = 'LoopMIDI Port'  # Adjust as needed
elif sys.platform == 'darwin':
    virtual_port_name = 'IAC Driver Bus 1'  # Adjust as needed
else:
    raise Exception("Unsupported platform")

midi_input_name = 'Ampero'  # Name of the MIDI input device to listen to

# Function to handle incoming SysEx messages
def handle_sysex(message):
    print(str(message))
    if list(message.data) == SYSEX_MESSAGE_1:
        print("Received SysEx Message 1")
        # Send MIDI note C4 to virtual port
        outport.send(mido.Message('note_on', note=60, velocity=64))
    elif list(message.data) == SYSEX_MESSAGE_2:
        print("Received SysEx Message 2")
        # Send MIDI note C#4 to virtual port
        outport.send(mido.Message('note_on', note=61, velocity=64))

# Function to create a virtual MIDI input port (if not already created)
def create_virtual_input():
    try:
        inport = mido.open_input(virtual_port_name)
    except IOError:
        # Create new virtual input port
        print(f"Creating virtual MIDI input port: {virtual_port_name}")
        inport = mido.open_input(virtual_port_name, virtual=True)
    return inport

# Main function to run the script
def main():
    global outport
    # Open a virtual MIDI output port
    outport = mido.open_output(virtual_port_name)

    # Create or open the virtual MIDI input port
    inport = create_virtual_input()

    # Open the specified MIDI input device
    try:
        ampero_inport = mido.open_input(midi_input_name)
    except IOError:
        raise Exception(f"Failed to open MIDI input device: {midi_input_name}")

    # Start a thread to listen for incoming MIDI messages
    threading.Thread(target=listen_for_messages, args=(ampero_inport,)).start()

    # Keep the script running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting...")
        inport.close()
        outport.close()
        ampero_inport.close()

# Function to listen for incoming MIDI messages
def listen_for_messages(inport):
    print(f"Listening for MIDI messages on {inport.name}")
    for message in inport:
        if message.type == 'sysex':
            handle_sysex(message)

if __name__ == "__main__":
    main()
