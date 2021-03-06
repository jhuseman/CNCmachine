EESchema Schematic File Version 4
LIBS:ArduinoShield-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "lun. 30 mars 2015"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 8950 1450 1    60   ~ 0
Vin
Text Label 9350 1450 1    60   ~ 0
IOREF
Text Label 8900 2500 0    60   ~ 0
A0
Text Label 8900 2600 0    60   ~ 0
A1
Text Label 8900 2700 0    60   ~ 0
A2
Text Label 8900 2800 0    60   ~ 0
A3
Text Label 8900 2900 0    60   ~ 0
A4(SDA)
Text Label 8900 3000 0    60   ~ 0
A5(SCL)
Text Label 10550 3000 0    60   ~ 0
0(Rx)
Text Label 10550 2800 0    60   ~ 0
2
Text Label 10550 2900 0    60   ~ 0
1(Tx)
Text Label 10550 2700 0    60   ~ 0
3(**)
Text Label 10550 2600 0    60   ~ 0
4
Text Label 10550 2500 0    60   ~ 0
5(**)
Text Label 10550 2400 0    60   ~ 0
6(**)
Text Label 10550 2300 0    60   ~ 0
7
Text Label 10550 2100 0    60   ~ 0
8
Text Label 10550 2000 0    60   ~ 0
9(**)
Text Label 10550 1900 0    60   ~ 0
10(**/SS)
Text Label 10550 1800 0    60   ~ 0
11(**/MOSI)
Text Label 10550 1700 0    60   ~ 0
12(MISO)
Text Label 10550 1600 0    60   ~ 0
13(SCK)
Text Label 10550 1400 0    60   ~ 0
AREF
NoConn ~ 9400 1600
Text Notes 8550 750  0    60   ~ 0
Shield for Arduino that uses\nthe same pin disposition\nlike "Uno" board Rev 3.
$Comp
L Connector_Generic:Conn_01x08 P1
U 1 1 56D70129
P 9600 1900
F 0 "P1" H 9600 2350 50  0000 C CNN
F 1 "Power" V 9700 1900 50  0000 C CNN
F 2 "Socket_Arduino_Uno:Socket_Strip_Arduino_1x08" V 9750 1900 20  0000 C CNN
F 3 "" H 9600 1900 50  0000 C CNN
	1    9600 1900
	1    0    0    -1  
$EndComp
Text Label 8650 1800 0    60   ~ 0
Reset
$Comp
L power:+3.3V #PWR01
U 1 1 56D70538
P 9150 1450
F 0 "#PWR01" H 9150 1300 50  0001 C CNN
F 1 "+3.3V" V 9150 1700 50  0000 C CNN
F 2 "" H 9150 1450 50  0000 C CNN
F 3 "" H 9150 1450 50  0000 C CNN
	1    9150 1450
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR02
U 1 1 56D707BB
P 9050 1350
F 0 "#PWR02" H 9050 1200 50  0001 C CNN
F 1 "+5V" V 9050 1550 50  0000 C CNN
F 2 "" H 9050 1350 50  0000 C CNN
F 3 "" H 9050 1350 50  0000 C CNN
	1    9050 1350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR03
U 1 1 56D70CC2
P 9300 3150
F 0 "#PWR03" H 9300 2900 50  0001 C CNN
F 1 "GND" H 9300 3000 50  0000 C CNN
F 2 "" H 9300 3150 50  0000 C CNN
F 3 "" H 9300 3150 50  0000 C CNN
	1    9300 3150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 56D70CFF
P 10300 3150
F 0 "#PWR04" H 10300 2900 50  0001 C CNN
F 1 "GND" H 10300 3000 50  0000 C CNN
F 2 "" H 10300 3150 50  0000 C CNN
F 3 "" H 10300 3150 50  0000 C CNN
	1    10300 3150
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x06 P2
U 1 1 56D70DD8
P 9600 2700
F 0 "P2" H 9600 2300 50  0000 C CNN
F 1 "Analog" V 9700 2700 50  0000 C CNN
F 2 "Socket_Arduino_Uno:Socket_Strip_Arduino_1x06" V 9750 2750 20  0000 C CNN
F 3 "" H 9600 2700 50  0000 C CNN
	1    9600 2700
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 P5
U 1 1 56D71177
P 10800 650
F 0 "P5" V 10900 650 50  0000 C CNN
F 1 "CONN_01X01" V 10900 650 50  0001 C CNN
F 2 "Socket_Arduino_Uno:Arduino_1pin" H 10721 724 20  0000 C CNN
F 3 "" H 10800 650 50  0000 C CNN
	1    10800 650 
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 P6
U 1 1 56D71274
P 10900 650
F 0 "P6" V 11000 650 50  0000 C CNN
F 1 "CONN_01X01" V 11000 650 50  0001 C CNN
F 2 "Socket_Arduino_Uno:Arduino_1pin" H 10900 650 20  0001 C CNN
F 3 "" H 10900 650 50  0000 C CNN
	1    10900 650 
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 P7
U 1 1 56D712A8
P 11000 650
F 0 "P7" V 11100 650 50  0000 C CNN
F 1 "CONN_01X01" V 11100 650 50  0001 C CNN
F 2 "Socket_Arduino_Uno:Arduino_1pin" V 11000 650 20  0001 C CNN
F 3 "" H 11000 650 50  0000 C CNN
	1    11000 650 
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 P8
U 1 1 56D712DB
P 11100 650
F 0 "P8" V 11200 650 50  0000 C CNN
F 1 "CONN_01X01" V 11200 650 50  0001 C CNN
F 2 "Socket_Arduino_Uno:Arduino_1pin" H 11024 572 20  0000 C CNN
F 3 "" H 11100 650 50  0000 C CNN
	1    11100 650 
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x08 P4
U 1 1 56D7164F
P 10000 2600
F 0 "P4" H 10000 2100 50  0000 C CNN
F 1 "Digital" V 10100 2600 50  0000 C CNN
F 2 "Socket_Arduino_Uno:Socket_Strip_Arduino_1x08" V 10150 2550 20  0000 C CNN
F 3 "" H 10000 2600 50  0000 C CNN
	1    10000 2600
	-1   0    0    -1  
$EndComp
Wire Notes Line
	8525 825  9925 825 
Wire Notes Line
	9925 825  9925 475 
Wire Wire Line
	9350 1450 9350 1700
Wire Wire Line
	9350 1700 9400 1700
Wire Wire Line
	9400 1900 9150 1900
Wire Wire Line
	9400 2000 9050 2000
Wire Wire Line
	9400 2300 8950 2300
Wire Wire Line
	9400 2100 9300 2100
Wire Wire Line
	9400 2200 9300 2200
Connection ~ 9300 2200
Wire Wire Line
	8950 2300 8950 1450
Wire Wire Line
	9050 2000 9050 1350
Wire Wire Line
	9150 1900 9150 1450
$Comp
L Connector_Generic:Conn_01x10 P3
U 1 1 56D721E0
P 10000 1600
F 0 "P3" H 10000 2150 50  0000 C CNN
F 1 "Digital" V 10100 1600 50  0000 C CNN
F 2 "Socket_Arduino_Uno:Socket_Strip_Arduino_1x10" V 10150 1600 20  0000 C CNN
F 3 "" H 10000 1600 50  0000 C CNN
	1    10000 1600
	-1   0    0    -1  
$EndComp
Wire Wire Line
	10200 2000 10550 2000
Wire Wire Line
	10200 1900 10550 1900
Wire Wire Line
	10200 1800 10550 1800
Wire Wire Line
	10200 1700 10550 1700
Wire Wire Line
	10200 1600 10550 1600
Wire Wire Line
	10200 1400 10550 1400
Wire Wire Line
	10200 1300 10550 1300
Wire Wire Line
	10200 1200 10550 1200
Wire Wire Line
	10200 1500 10300 1500
Wire Wire Line
	10300 1500 10300 3150
Wire Wire Line
	9300 2100 9300 2200
Wire Wire Line
	9300 2200 9300 3150
Wire Notes Line
	8500 500  8500 3450
Wire Notes Line
	8500 3450 11200 3450
Wire Wire Line
	9400 1800 8650 1800
Text Notes 9700 1600 0    60   ~ 0
1
Wire Notes Line
	11200 1000 10700 1000
Wire Notes Line
	10700 1000 10700 500 
$Comp
L Connector_Generic:Conn_01x04 J5
U 1 1 5C341FD6
P 6400 1600
F 0 "J5" H 6480 1592 50  0000 L CNN
F 1 "Conn_01x04" H 6480 1501 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical" H 6400 1600 50  0001 C CNN
F 3 "~" H 6400 1600 50  0001 C CNN
	1    6400 1600
	1    0    0    -1  
$EndComp
Text Label 6000 1500 0    50   ~ 0
RX
Text Label 6000 1600 0    50   ~ 0
TX
Text Label 6000 1700 0    50   ~ 0
GND
Text Label 6000 1800 0    50   ~ 0
5V
$Comp
L power:GND #PWR0101
U 1 1 5C3451E8
P 5550 1950
F 0 "#PWR0101" H 5550 1700 50  0001 C CNN
F 1 "GND" H 5555 1777 50  0000 C CNN
F 2 "" H 5550 1950 50  0001 C CNN
F 3 "" H 5550 1950 50  0001 C CNN
	1    5550 1950
	1    0    0    -1  
$EndComp
Text GLabel 8700 1450 0    50   Input ~ 0
5V
Text GLabel 5800 1800 0    50   Input ~ 0
5V
Text GLabel 10900 3000 2    50   Input ~ 0
ardRX
Text GLabel 10900 2900 2    50   Input ~ 0
ardTX
Text GLabel 10900 2300 2    50   Input ~ 0
xpulse
Text GLabel 10900 2500 2    50   Input ~ 0
ypulse
Text GLabel 10900 2700 2    50   Input ~ 0
zpulse
Text GLabel 10900 2400 2    50   Input ~ 0
xdir
Text GLabel 10900 2600 2    50   Input ~ 0
ydir
Text GLabel 10900 2800 2    50   Input ~ 0
zdir
Text GLabel 8700 2500 0    50   Input ~ 0
xenable
Text GLabel 8700 2600 0    50   Input ~ 0
yenable
Text GLabel 8700 2700 0    50   Input ~ 0
zenable
Text GLabel 8700 3000 0    50   Input ~ 0
BTN
Text GLabel 8700 2800 0    50   Input ~ 0
xdir_rev
Wire Notes Line
	6350 400  6350 3350
Text GLabel 5200 2950 2    50   Input ~ 0
xenable
Text GLabel 5200 3350 2    50   Input ~ 0
yenable
Text GLabel 5200 3750 2    50   Input ~ 0
zenable
Text GLabel 5200 4150 2    50   Input ~ 0
xenable
Text GLabel 5200 4350 2    50   Input ~ 0
xpulse
Text GLabel 5200 4250 2    50   Input ~ 0
xdir_rev
Text GLabel 4950 1600 0    50   Input ~ 0
ardRX
Text GLabel 4950 1500 0    50   Input ~ 0
ardTX
Text GLabel 5200 3150 2    50   Input ~ 0
xpulse
Text GLabel 5200 3550 2    50   Input ~ 0
ypulse
Text GLabel 5200 3950 2    50   Input ~ 0
zpulse
Text GLabel 5200 3050 2    50   Input ~ 0
xdir
Text GLabel 5200 3450 2    50   Input ~ 0
ydir
Text GLabel 5200 3850 2    50   Input ~ 0
zdir
Wire Wire Line
	10200 2300 10900 2300
Wire Wire Line
	10200 2400 10900 2400
Wire Wire Line
	10200 2500 10900 2500
Wire Wire Line
	10200 2600 10900 2600
Wire Wire Line
	10200 2700 10900 2700
Wire Wire Line
	10200 2800 10900 2800
Wire Wire Line
	10200 2900 10900 2900
Wire Wire Line
	10200 3000 10900 3000
Wire Wire Line
	8700 3000 9400 3000
Wire Wire Line
	8700 2800 9400 2800
Wire Wire Line
	8700 2700 9400 2700
Wire Wire Line
	8700 2600 9400 2600
Wire Wire Line
	8700 2500 9400 2500
Wire Wire Line
	8700 1450 8950 1450
Wire Wire Line
	5800 1800 6200 1800
Wire Wire Line
	5550 1700 5550 1950
Wire Wire Line
	5550 1700 5700 1700
$Comp
L Device:R R1
U 1 1 5C359247
P 5300 1350
F 0 "R1" H 5370 1396 50  0000 L CNN
F 1 "10K" H 5370 1305 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5230 1350 50  0001 C CNN
F 3 "~" H 5300 1350 50  0001 C CNN
	1    5300 1350
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5C3592DC
P 5500 1350
F 0 "R2" H 5570 1396 50  0000 L CNN
F 1 "10K" H 5570 1305 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5430 1350 50  0001 C CNN
F 3 "~" H 5500 1350 50  0001 C CNN
	1    5500 1350
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 5C359F6C
P 5700 1350
F 0 "R3" H 5770 1396 50  0000 L CNN
F 1 "10K" H 5770 1305 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 5630 1350 50  0001 C CNN
F 3 "~" H 5700 1350 50  0001 C CNN
	1    5700 1350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5500 1500 5300 1500
Wire Wire Line
	5300 1500 4950 1500
Connection ~ 5300 1500
Wire Wire Line
	5300 1200 5500 1200
Wire Wire Line
	5500 1200 5700 1200
Connection ~ 5500 1200
Wire Wire Line
	5700 1500 5700 1700
Connection ~ 5700 1700
Wire Wire Line
	5700 1700 6200 1700
Wire Wire Line
	5900 1500 5900 1200
Wire Wire Line
	5900 1200 5700 1200
Wire Wire Line
	5900 1500 6200 1500
Connection ~ 5700 1200
Wire Wire Line
	4950 1600 6200 1600
$Comp
L Connector:Screw_Terminal_01x04 J1
U 1 1 5C362986
P 4800 3050
F 0 "J1" H 4720 2625 50  0000 C CNN
F 1 "Screw_Terminal_01x04" H 4720 2716 50  0000 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05504HBWC_1x04_P5.00mm_Horizontal" H 4800 3050 50  0001 C CNN
F 3 "~" H 4800 3050 50  0001 C CNN
	1    4800 3050
	-1   0    0    1   
$EndComp
$Comp
L Connector:Screw_Terminal_01x04 J2
U 1 1 5C367497
P 4800 3450
F 0 "J2" H 4720 3025 50  0000 C CNN
F 1 "Screw_Terminal_01x04" H 4720 3116 50  0000 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05504HBWC_1x04_P5.00mm_Horizontal" H 4800 3450 50  0001 C CNN
F 3 "~" H 4800 3450 50  0001 C CNN
	1    4800 3450
	-1   0    0    1   
$EndComp
$Comp
L Connector:Screw_Terminal_01x04 J3
U 1 1 5C36872A
P 4800 3850
F 0 "J3" H 4720 3425 50  0000 C CNN
F 1 "Screw_Terminal_01x04" H 4720 3516 50  0000 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05504HBWC_1x04_P5.00mm_Horizontal" H 4800 3850 50  0001 C CNN
F 3 "~" H 4800 3850 50  0001 C CNN
	1    4800 3850
	-1   0    0    1   
$EndComp
$Comp
L Connector:Screw_Terminal_01x04 J4
U 1 1 5C368731
P 4800 4250
F 0 "J4" H 4720 3825 50  0000 C CNN
F 1 "Screw_Terminal_01x04" H 4720 3916 50  0000 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05504HBWC_1x04_P5.00mm_Horizontal" H 4800 4250 50  0001 C CNN
F 3 "~" H 4800 4250 50  0001 C CNN
	1    4800 4250
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5C36999E
P 5800 4450
F 0 "#PWR0102" H 5800 4200 50  0001 C CNN
F 1 "GND" H 5805 4277 50  0000 C CNN
F 2 "" H 5800 4450 50  0001 C CNN
F 3 "" H 5800 4450 50  0001 C CNN
	1    5800 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 4050 5800 4050
Wire Wire Line
	5000 3650 5800 3650
Wire Wire Line
	5800 3250 5000 3250
Wire Wire Line
	5000 2850 5800 2850
Wire Wire Line
	5000 2950 5200 2950
Wire Wire Line
	5800 2850 5800 3250
Connection ~ 5800 3250
Wire Wire Line
	5800 3250 5800 3650
Connection ~ 5800 3650
Wire Wire Line
	5800 3650 5800 4050
Wire Wire Line
	5200 3050 5000 3050
Wire Wire Line
	5000 3150 5200 3150
Wire Wire Line
	5200 3350 5000 3350
Wire Wire Line
	5000 3450 5200 3450
Wire Wire Line
	5200 3550 5000 3550
Wire Wire Line
	5000 3750 5200 3750
Wire Wire Line
	5200 3850 5000 3850
Wire Wire Line
	5000 3950 5200 3950
Wire Wire Line
	5200 4150 5000 4150
Wire Wire Line
	5000 4250 5200 4250
Wire Wire Line
	5200 4350 5000 4350
Wire Wire Line
	5800 4450 5800 4050
Connection ~ 5800 4050
$Comp
L power:GND #PWR0103
U 1 1 5C3B83DB
P 10500 850
F 0 "#PWR0103" H 10500 600 50  0001 C CNN
F 1 "GND" H 10505 677 50  0000 C CNN
F 2 "" H 10500 850 50  0001 C CNN
F 3 "" H 10500 850 50  0001 C CNN
	1    10500 850 
	1    0    0    -1  
$EndComp
Wire Wire Line
	10500 850  10800 850 
Wire Wire Line
	10800 850  10900 850 
Connection ~ 10800 850 
Wire Wire Line
	10900 850  11000 850 
Connection ~ 10900 850 
Wire Wire Line
	11000 850  11100 850 
Connection ~ 11000 850 
$Comp
L Connector:Screw_Terminal_01x04 J6
U 1 1 5C3C93BE
P 7600 4650
F 0 "J6" H 7680 4642 50  0000 L CNN
F 1 "Screw_Terminal_01x04" H 7680 4551 50  0000 L CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05504HBWC_1x04_P5.00mm_Horizontal" H 7600 4650 50  0001 C CNN
F 3 "~" H 7600 4650 50  0001 C CNN
	1    7600 4650
	1    0    0    -1  
$EndComp
Text Label 7200 4550 0    50   ~ 0
GND
Text Label 7200 4650 0    50   ~ 0
REL
Text Label 7200 4750 0    50   ~ 0
BTN
Text Label 7200 4850 0    50   ~ 0
5V
$Comp
L power:GND #PWR0104
U 1 1 5C3CBCFA
P 7050 4250
F 0 "#PWR0104" H 7050 4000 50  0001 C CNN
F 1 "GND" H 7055 4077 50  0000 C CNN
F 2 "" H 7050 4250 50  0001 C CNN
F 3 "" H 7050 4250 50  0001 C CNN
	1    7050 4250
	1    0    0    -1  
$EndComp
Text GLabel 7050 4850 0    50   Input ~ 0
5V
Wire Wire Line
	7400 4650 7200 4650
Wire Wire Line
	7400 4750 7200 4750
Wire Wire Line
	7050 4850 7400 4850
Wire Wire Line
	6950 4550 6950 4450
Wire Wire Line
	6950 4250 7050 4250
Wire Wire Line
	6950 4550 7400 4550
Wire Wire Line
	7200 4650 7200 4750
$Comp
L Device:R R4
U 1 1 5C3DEFF2
P 6750 4600
F 0 "R4" H 6820 4646 50  0000 L CNN
F 1 "10K" H 6820 4555 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P7.62mm_Horizontal" V 6680 4600 50  0001 C CNN
F 3 "~" H 6750 4600 50  0001 C CNN
	1    6750 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	7200 4750 6750 4750
Connection ~ 7200 4750
Wire Wire Line
	6750 4450 6950 4450
Connection ~ 6950 4450
Wire Wire Line
	6950 4450 6950 4250
Text GLabel 6550 4750 0    50   Input ~ 0
BTN
Text Notes 10850 1000 0    60   ~ 0
Holes
Text Label 10550 1200 0    60   ~ 0
A5(SCL)-2
Text Label 10550 1300 0    60   ~ 0
A4(SDA)-2
Wire Wire Line
	6550 4750 6750 4750
Connection ~ 6750 4750
Wire Wire Line
	10550 2100 10200 2100
Wire Wire Line
	8900 2900 9400 2900
NoConn ~ 8900 2900
NoConn ~ 10550 2100
NoConn ~ 10550 2000
NoConn ~ 10550 1900
NoConn ~ 10550 1800
NoConn ~ 10550 1700
NoConn ~ 10550 1600
NoConn ~ 10550 1400
NoConn ~ 10550 1300
NoConn ~ 10550 1200
$EndSCHEMATC
