from dataclasses import dataclass


@dataclass
class KellyMessage:
    command:int
    length:int
    data:bytearray