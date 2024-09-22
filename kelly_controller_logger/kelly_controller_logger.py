import serial
# import tempfile
import datetime
import time
import csv

from messages import *

class KellyControllerLogger:

    __BAUDRATE = 19200
    __WRITE_TIMEOUT = 0.1
    __READ_TIMEOUT = 0.1

    def __init__(self, port_name):
        self.port_name = port_name
        self.command_message = CommandMessage()
        self.feedback_message = FeedbackMessage()
        self.encoder_message = EncoderMessage()
        self.metadata = {'id':0,'time_unix':0, 'time_text':''}
        self.headers = list(self.metadata.keys())
        self.headers.extend(list(self.command_message.asdict().keys()))
        self.headers.extend(list(self.feedback_message.asdict().keys()))
        self.headers.extend(list(self.encoder_message.asdict().keys()))
        self.headers.remove('message_id')
        self.headers.remove('length')

    def run(self, f, frequency_hz=10):
        with serial.Serial(self.port_name, baudrate=self.__BAUDRATE, write_timeout=self.__WRITE_TIMEOUT, timeout=self.__READ_TIMEOUT) as ser:
            print("Logger Serial Opened")
            writer = csv.DictWriter(f, fieldnames=self.headers, extrasaction='ignore')
            if f.tell() == 0:#beginning of file, write the headers
                writer.writeheader()
            while True:
                try:
                    self.metadata['time_unix'] = datetime.datetime.now()
                    self.metadata['time_text'] = self.metadata['time_unix'].strftime(f"%Y-%m-%dT%H:%M:%S")
                    success = KellyControllerLogger.poll_message(ser,self.command_message) and \
                        KellyControllerLogger.poll_message(ser,self.feedback_message) and \
                        KellyControllerLogger.poll_message(ser,self.encoder_message)
                    if success:
                        combined = self.metadata | self.command_message.asdict() | self.feedback_message.asdict() | self.encoder_message.asdict()
                        writer.writerow(combined)
                        #print("All Messages Received!")
                        self.metadata['id'] += 1
                    else:
                        print("Failed to receive or parse at least one message")
                except Exception as ex:
                    print("Error Updating Messages: %s"%str(ex))
                if frequency_hz <= 0:
                    print("Frequency value is invalid")
                    return #error state
                time.sleep(1/frequency_hz)
                if self.metadata['id'] % (5*frequency_hz) == 0:
                    f.flush()
                
            

    def poll_message(ser:serial.Serial, message:KellyMessage):
        command = bytearray(3)
        command[0] = command[2] = message.message_id
        command[1] = 0
        #print("polling 0x%02x"%message.message_id)
        ser.write(command)
        time.sleep(0.01)#yield
        #print("reading response...")
        response = ser.read(message.length+3)
        if len(response) == message.length+3:
            return message.load_message(response)
        print("response length incorrect: %u != %u!"%(len(response),message.length+3))
        return False
