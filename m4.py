import serial
import serial.tools.list_ports
import logging

import bb_log

bat_log = bb_log.get_log()

def search_comports(serial_number):

    for port in serial.tools.list_ports.comports():
        
        if type(port.serial_number) != str:
            continue
        
        if port.serial_number == serial_number:
            return port
    
    return "None"

class M4:
    
    def __init__(self, serial_number, page_size):
    
        self.page_size = page_size
                
        self.port = search_comports(serial_number)
                    
        if self.port == "None":
            bat_log.critical(f"Could not find device with serial number {serial_number}")
            exit()
            
        
        self.sercom = serial.Serial(self.port.device)
            
        bat_log.info(f"Found device {serial_number} on {self.port.device}")
            
        self.reset()
        
    def reset(self):

        self.sercom.setDTR(False)
        
        time.sleep(1)
        
        self.sercom.flushInput()
        self.sercom.setDTR(True)
    
    def write(self, packet):
        self.sercom.write(packet)
    
    def read(self, length):
        return self.sercom.read(length)