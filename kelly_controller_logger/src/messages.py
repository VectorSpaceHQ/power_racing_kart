from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class KellyMessage:
    command:int
    length:int

    def __init__(self, command, length):
        self.command = command
        self.length = length
        self.data = bytearray(3+length)

    def get_param(self, param):
        if param > self.length or param < 0:
            return 0
        return self.data[param]
    
    def load_message(self,message):
        if len(message) != self.length+3:
            return False
        if message[0] != self.command:
            return False
        if message[1] != self.length:
            return False
        self.data = message[2:self.length+2]
        checksum = 0
        for b in message[0:self.length+2]:
            checksum += b
        if checksum % 256 != message[self.length+2]:
            return False
        return self.update_fields()
    
    def update_fields(self):
        return True
    
    def asdict(self):
        return asdict(self)



@dataclass
class CommandMessage(KellyMessage):
    break_ad:int
    tps_ad:int
    sp_ad:int
    power_ad:int
    vs_ad:int
    bplus_ad:int
    temp_ad:int
    ia_ad:int
    ib_ad:int
    ic_ad:int
    va_ad:int
    vb_ad:int
    vc_ad:int
    htemp_ad:int
    vplus_ad:int
    ltemp_ad:int

    __BREAK_AD  = 0
    __TPS_AD    = 1
    __SP_AD     = 2
    __POWER_AD  = 3
    __VS_AD     = 4
    __BPLUS_AD  = 5
    __TEMP_AD   = 6
    __IA_AD     = 7
    __IB_AD     = 8
    __IC_AD     = 9
    __VA_AD     = 10
    __VB_AD     = 11
    __VC_AD     = 12
    __HTEMP_AD  = 13
    __VPLUS_AD  = 14
    __LTEMP_AD  = 15

    __COMMAND = 0x1b
    __LENGTH = 16

    def __init__(self):
        super().__init__(self.__COMMAND, self.__LENGTH)

    def update_fields(self):
        self.break_ad   = self.get_param(self.__BREAK_AD)
        self.tps_ad     = self.get_param(self.__TPS_AD)
        self.sp_ad      = self.get_param(self.__SP_AD)
        self.power_ad   = self.get_param(self.__POWER_AD)
        self.vs_ad      = self.get_param(self.__VS_AD)
        self.bplus_ad   = self.get_param(self.__BPLUS_AD)
        self.temp_ad    = self.get_param(self.__TEMP_AD)
        self.ia_ad      = self.get_param(self.__IA_AD)
        self.ib_ad      = self.get_param(self.__IB_AD)
        self.ic_ad      = self.get_param(self.__IC_AD)
        self.va_ad      = self.get_param(self.__VA_AD)
        self.vb_ad      = self.get_param(self.__VB_AD)
        self.vc_ad      = self.get_param(self.__VC_AD)
        self.htemp_ad   = self.get_param(self.__HTEMP_AD)
        self.vplus_ad   = self.get_param(self.__VPLUS_AD)
        self.ltemp_ad   = self.get_param(self.__LTEMP_AD)
        return True

@dataclass
class FeedbackMessage(KellyMessage):
    pwr_volt:int
    bplus_volt:int
    va_volt:int
    vb_volt:int
    vc_volt:int
    pwm_duty:int
    vplus_volt:int
    high_temp:int
    low_temp:int
    motor_temp:int
    brake_switch:int
    rev_switch:int
    foot_switch:int
    sc_level:int
    sb_level:int
    sa_level:int

    __PWR_VOLT      = 0
    __BPLUS_VOLT    = 1
    __VA_VOLT       = 2
    __VB_VOLT       = 3
    __VC_VOLT       = 4
    __PWM_DUTY      = 5
    __VPLUS_VOLT    = 6
    __HIGH_TEMP     = 7
    __LOW_TEMP      = 8
    __MOTOR_TEMP    = 9
    __BRAKE_SWITCH  = 10
    __REV_SWITCH    = 11
    __FOOT_SWITCH   = 12
    __SC_LEVEL      = 13
    __SB_LEVEL      = 14
    __SA_LEVEL      = 15

    __COMMAND = 0x33
    __LENGTH = 16

    def __init__(self):
        super().__init__(self.__COMMAND, self.__LENGTH)

    def update_fields(self):
        self.pwr_volt       = self.get_param(self.__PWR_VOLT)
        self.bplus_volt     = self.get_param(self.__BPLUS_VOLT)
        self.va_volt        = self.get_param(self.__VA_VOLT)
        self.vb_volt        = self.get_param(self.__VB_VOLT)
        self.vc_volt        = self.get_param(self.__VC_VOLT)
        self.pwm_duty       = self.get_param(self.__PWM_DUTY)
        self.vplus_volt     = self.get_param(self.__VPLUS_VOLT)
        self.high_temp      = self.get_param(self.__HIGH_TEMP)
        self.low_temp       = self.get_param(self.__LOW_TEMP)
        self.motor_temp     = self.get_param(self.__MOTOR_TEMP)
        self.brake_switch   = self.get_param(self.__BRAKE_SWITCH)
        self.rev_switch     = self.get_param(self.__REV_SWITCH)
        self.foot_switch    = self.get_param(self.__FOOT_SWITCH)
        self.sc_level       = self.get_param(self.__SC_LEVEL)
        self.sb_level       = self.get_param(self.__SB_LEVEL)
        self.sa_level       = self.get_param(self.__SA_LEVEL)
        return True

    
@dataclass
class EncoderMessage(KellyMessage):
    thing_a:int
    thing_b:int
    thing_c:int
    motor_speed:int
    pcb_temp:int
    forward_switch:int
    two_speed:int
    reserved_7:int
    reserved_8:int
    reserved_9:int
    reserved_a:int
    reserved_b:int
    reserved_c:int

    __THING_A           = 0
    __THING_B           = 1
    __THING_C           = 2
    __MOTOR_SPEED       = 3
    __PCB_TEMP          = 4
    __FORWARD_SWITCH    = 5
    __TWO_SPEED         = 6
    __RESERVED_7        = 7
    __RESERVED_8        = 8
    __RESERVED_9        = 9
    __RESERVED_A        = 10
    __RESERVED_B        = 11
    __RESERVED_C        = 12

    __COMMAND = 0x34
    __LENGTH = 13

    def __init__(self):
        super().__init__(self.__COMMAND, self.__LENGTH)

    def update_fields(self):
        self.thing_a        = self.get_param(self.__THING_A)
        self.thing_b        = self.get_param(self.__THING_B)
        self.thing_c        = self.get_param(self.__THING_C)
        self.motor_speed    = self.get_param(self.__MOTOR_SPEED)
        self.pcb_temp       = self.get_param(self.__PCB_TEMP)
        self.forward_switch = self.get_param(self.__FORWARD_SWITCH)
        self.two_speed      = self.get_param(self.__TWO_SPEED)
        self.reserved_7     = self.get_param(self.__RESERVED_7)
        self.reserved_8     = self.get_param(self.__RESERVED_8)
        self.reserved_9     = self.get_param(self.__RESERVED_9)
        self.reserved_a     = self.get_param(self.__RESERVED_A)
        self.reserved_b     = self.get_param(self.__RESERVED_B)
        self.reserved_c     = self.get_param(self.__RESERVED_C)
        return True