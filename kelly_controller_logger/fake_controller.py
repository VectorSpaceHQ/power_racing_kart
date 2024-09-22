import serial
import time
from collections import deque
from messages import *


class FakeKellyController:

    __BAUDRATE = 19200
    __READ_TIMEOUT = 0.01
    __WRITE_TIMEOUT = 0.1

    __example_command_data = b'\x1b\x10\x00\x2a\x00\x93\x7b\x93\x63\x81\x81\x81\x00\x00\x00\xff\xcc\xef\x96'
    __example_feedback_data = b'\x33\x10\x36\x36\x00\x00\x00\x00\x0c\x32\x1f\x00\x01\x01\x01\x00\x00\x01\x10'
    __example_encoder_data = b'\x34\x0d\x00\x00\x00\x00\x23\x01\x01\x00\x00\x00\x00\x00\x00\x66'

    def __init__(self, port_name):
        self.port_name = port_name
        self.command_message = CommandMessage()
        self.command_message.load_message(self.__example_command_data)
        self.feedback_message = FeedbackMessage()
        self.feedback_message.load_message(self.__example_feedback_data)
        self.encoder_message = EncoderMessage()
        self.encoder_message.load_message(self.__example_encoder_data)



    def run(self):
        byte_queue = deque(maxlen=3)
        messages = [self.command_message, self.feedback_message, self.encoder_message]
        with serial.Serial(self.port_name,baudrate=self.__BAUDRATE, timeout=self.__READ_TIMEOUT, write_timeout=self.__WRITE_TIMEOUT) as ser:
            print("Controller serial opened: %s"%str(ser.is_open))
            while True:
                b = ser.read()
                if len(b) > 0:
                    bint = int.from_bytes(b)
                    #print("Controller received 0x%02x"%bint)
                    byte_queue.append(bint) #add to right
                    if len(byte_queue) == 3:
                        if byte_queue[0] == byte_queue[2] and byte_queue[1] == 0:
                            #print("Controller received command for message 0x%02x"%bint)
                            for m in messages:
                                if m.message_id == bint:
                                    #print("Sending message %s"%str(m))
                                    bytes_written = ser.write(m.get_message())
                                    if bytes_written != m.length+3:
                                        print("Error sending message")
                            byte_queue.clear()
                        else:
                            print("Controller received unknown command %02x"%bint)
                time.sleep(0)#yield





    
    

