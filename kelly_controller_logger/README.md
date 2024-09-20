# Kelly Controller Data Logger

Data logger designed to work with the [Kelly Controller KBS-X Line](https://kellycontroller.com/shop/kbs/)

# Data Format

After snooping the serial communication between the Kelly PC app and the controller, multiple data frames (telegrams?) were found that appear to comprise the information seen in the "data view" tab within the kelly PC and android apps.

*Note that the Kelly App connects using 19200 baud, no stop bit, and non-parity settings.*

The host app polls the controller with a 3 byte message. The first and third bytes are both the "Frame ID" and the middle (2nd) byte is 0x00. Three relevant frame types were identified (names are assumed):
* __0x1b__ "Command Data" (16 bytes)
* __0x33__ "Feedback Data" (16 bytes)
* __0x34__ "Encoder Data" (13 bytes)

The controller responds to these commands in a standard way:
1. The first byte is a repeat of the command byte
1. The second byte indicates the length of the data being sent
1. The next n bytes are the data
1. The final byte is a checksum, calculated by adding up all of the bytes in the message (including the command byte and length byte) and returning the remainder (modulo 256)

An example poll and response sequence might be:
```
PC or App:  0x1b001b
Controller: 0x1b10002a00937b9363818181000000ffccef96
```

The following sections contain details on the three frames I was able to correlate with fields in the Kelly app. I do not know what all of these fields mean, or what the units necessarily are. I have included typical values when idle for a KBS48121X (52V battery). Feedback is welcome!

## Command Data (0x1b)
This message frame appears to have a lot of info related to the commands of the control loop (internal and external) along with various limits and thresholds.

| Byte Number   | Example Value | Field Name    | Units     | Description 
|---------------|---------------|---------------|-----------|-------------
| 0x00          | 0x00 = False  | Break_AD      | BOOL      | Breaking Active? could be analog breaking power?
| 0x01          | 0x2a = 42     | TPS_AD        | UINT8     | Throttle Position??
| 0x02          | 0x00 = 0      | SP_AD         | UINT8     | Speed Setpoint?
| 0x03          | 0x93 = 147    | Power_AD      | UINT8?    | ?
| 0x04          | 0x7b = 123    | VS_AD         | UINT8?    | ?
| 0x05          | 0x93 = 147    | B+_AD         | UINT8?    | ?
| 0x06          | 0x63 = 99     | Temp_AD       | UINT8?    | ?
| 0x07          | 0x81 = 129    | IA_AD         | INT8?     | A phase current? maybe bidirectional balanced around 0x80 = 0 instead of a true signed byte (MSBit is a flag?)
| 0x08          | 0x81 = 129    | IB_AD         | INT8?     | B phase current? maybe bidirectional balanced around 0x80 = 0 instead of a true signed byte (MSBit is a flag?)
| 0x09          | 0x81 = 129    | IC_AD         | INT8?     | C phase current? maybe bidirectional balanced around 0x80 = 0 instead of a true signed byte (MSBit is a flag?)
| 0x0a          | 0x00 = 0      | VA_AD         | UINT8     | A phase voltage setpoint?
| 0x0b          | 0x00 = 0      | VB_AD         | UINT8     | B phase voltage setpoint?
| 0x0c          | 0x00 = 0      | VC_AD         | UINT8     | C phase voltage setpoint?
| 0x0d          | 0xff = 255    | Htemp_AD      | ?         | High temp limit?
| 0x0e          | 0xcc = 128+52 | V+_AD         | UINT7+Flag| measured battery voltage plus a flag on the most significant bit? although V+ i thought was the accessory voltage...
| 0x0f          | 0xef = 239    | Ltemp_AD      | ?         | Low temp limit?

## Feedback Data (0x33)
This message frame appears to have a lot of measured values reported.

| Byte Number   | Example Value | Field Name    | Units     | Description 
|---------------|---------------|---------------|-----------|-------------
| 0x00          | 54            | PWR_Volt      | UINT8     | Main power voltage
| 0x01          | 54            | B+ Volt       | UINT8     | Battery line voltage
| 0x02          | 0             | VA Volt       | UINT8     | A phase voltage?
| 0x03          | 0             | VB Volt       | UINT8     | B phase voltage?
| 0x04          | 0             | VC Volt       | UINT8     | C phase voltage?
| 0x05          | 0             | PWM Duty      | UINT8?    | Something about the way variable voltage is achieved in each phase? larger is faster?
| 0x06          | 12            | V+ Volt       | UINT8     | Voltage on the logic/accessory components?
| 0x07          | 50            | High Temp     | UINT8     | Highest temp measured this power cycle?
| 0x08          | 31            | Low Temp      | UINT8     | Lowest temp measured this power cycle?
| 0x09          | 0             | Motor Temp    | UINT8     | Current motor temperature (might not be measured in all models?)
| 0x0a          | 1             | Brake Switch  | BOOL      | Brake switch level (True means brake not engaged)
| 0x0b          | 1             | Rev Switch    | BOOL      | Reverse switch level (True means forward)
| 0x0c          | 1             | Foot Switch   | BOOL      | Foot switch level (True means ?)
| 0x0d          | 0             | SC Level      | BOOL?     | C phase...?
| 0x0e          | 0             | SB Level      | BOOL?     | B phase...?
| 0x0f          | 0             | SA Level      | BOOL?     | A phase...?

## Encoder Data? (0x34)
This message frame appears to have somethings related to the motor and its speed. maybe even something about the hall effector sensors?

| Byte Number   | Example Value | Field Name    | Units     | Description 
|---------------|---------------|---------------|-----------|-------------
| 0x00          | 0             | ?             | ?         | ? Hall effect values for phase A/C?
| 0x01          | 0             | ?             | ?         | ? Hall effect values for phase B?
| 0x02          | 0             | ?             | ?         | ? Hall effect values for phase C/A?
| 0x03          | 0             | Motor Speed   | ?         | Motor speed measured by sensors?
| 0x04          | 35            | PCB Temp      | UINT8     | Current PCB Temp (Celcius)
| 0x05          | 1             | Forward Switch| BOOL      | True if direction selected is forward
| 0x06          | 1             | Two Speed     | BOOL      | True if ????
| 0x07          | 0             | Reserved      |
| 0x08          | 0             | Reserved      |
| 0x09          | 0             | Reserved      |
| 0x0a          | 0             | Reserved      |
| 0x0b          | 0             | Reserved      |
| 0x0c          | 0             | Reserved      |
