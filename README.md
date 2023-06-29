# Gamma spectroscopy

## Introduction
Sooner or later your fingers will get itchy: once you deal with Geiger counters and with radioactivity, then you just want to try out at some time also gamma spectroscopy. But as a normal electronics hobbyist you usually have a lot of respect for that pure physics stuff with photomultipliers, scintillators and so forth. But once you have dared to cross this barrier, then you ask yourself why not started earlier.

My earlier Geiger counter projects using simple ionization tubes as detectors can only be used to count pulses caused by a passing gamma-ray and deriving the ionizing radiation dose. This project is doing the same, but an additional feature is the capability of measuring also the intensities of the pulses. The intensities of the pulses can be clearly assigned to gamma energies [unit keV]. Most radioactive sources produce gamma rays, which are of various energies and intensities. When these emissions are measured by this spectroscopy project, a gamma-ray energy spectrum can be produced afterwards from the collected data.

As we know now that a simple ionization tube as detector is not capable to measure gamma-ray energies, some other type of gamma-ray detector needs to come into game: a SiPM (Silicon Photo Multiplier) together with a scintillator.

## Scintillator

A scintillator is a material that is excited to glow in the visible range by incoming ionizing particles or radiation. I.e. it releases the absorbed energy in the form of light. A tight coupled photo multiplier is used to measure the sparkling of the emitted light. There exist various types of scintillators for different materials, wavelengths and sensitivities. The widely used NaI(Tl) (thallium-doped sodium iodide) inorganic crystal is also used in this project. The scintillation wavelength of the emitted photons fits to the used blue-sensitive photo multiplier. Incoming high energy radiation, i.e. in our case gamma photons, interact with the NaI(Tl) material and dissipate their kinetic energy to produce electron-hole pairs. The recombination of these electron-hole pairs leads to very short (few microseconds) visible light emissions. The presence of thallium significantly increases the light emission of the crystal and is referred to as an activator for the crystal.

<img src="/Images/image01.png" alt="" height="300" title="Scintillator With SiPM">

The scintillator together with the photo multiplier must be housed in an absolutely light-tight housing so that the ambient light does not falsify the measurements. For this it is best to use some thin aluminum foil and black tape. The size of the used NaI(Tl) crystal is 10x10x30mm. In the following picture you see an example how the scintillator could look like.

<img src="/Images/image02.png" alt="" height="300" title="Scintillator NaI(Tl) Crystal">

## Photo Multiplier

Typically photomultiplier tubes were used earlier for gamma spectroscopy. Since several years they have been replaced more and more by silicon photomultipliers (SiPMs). The most important benefit of a SiPM is that it doesn't need a high voltage negative power supply of about -1kV like a photomultier tube needs. Therefore also no complicated circuit wiring is required. SiPMs consist of an array of Single Photon Avalanche Diodes (SPAD) which are reverse-biased with sufficient voltage to operate in avalanche mode, enabling each microcell of the array to be sensitive to single photons. 

<img src="/Images/image03.png" alt="" height="300" title="Single Photon Avalanche Diodes">

The used SiPM is an [Onsemi MicroFC-30065-SMT](/Datasheets/MICROC-SERIES-D.pdf) device which has ~19000 microcells (SPADs) on an active area of 36mm². See a photo of this SiPM in the following photo.

<img src="/Photos/photo01.jpg" alt="" height="300" title="MicroFC-30065-SMT SiPM">

The gain factor of this SiPM is quite high at 3 x 10E6. The reverse-biased voltage (+Vbias) is set to +28V which is available at `TP6` in the schematic of the SIPM module. This bias voltage is also temperature compensated with an NTC (R4) on the feedback loop. The cathode of the SIPM is connected to `TP6` whereas the anode is connected to `TP7` (in reverse direction). Finally the pulses at `TP7` are preamplified by a non-inverting buffer (OPAMP AD8055) and coupled out with 100 Ohm. The full schematic of the SiPM module can be seen in following picture.

<img src="/Schematics/SIPMmodule.png" alt="" height="500" title="SiPM Module full schematics">

I got the chance to get a fully assembled detector module containing the scintiallator crystal coupled to the SiPM with the biasing and preamp board in light tight housing. In the following see some photos of my detector module.

<img src="/Photos/photo02.jpg" alt="" height="300" title="Scintillator wrapped with aluminium foil and coupled to the SiPM module PCB">

<img src="/Photos/photo03.jpg" alt="" height="300" title="Completely closed SiPM module with connection cables">

The connections of the detector module are:
* Red: +5~9Vcc
* Black: GND
* Yellow: pulse output

## Schematic

The following picture shows the complete schematic including the preamplifier, the sample & hold circuit with the peak detector, the pulse discriminator, the analog-digital converter and the microcontroller. The SiPM module is connected to the `SiPM Module Connector`. Under the given conditions hardware components with the following limitations have been selected:

* as the cicuit operates only with 3.3 Volt the OPAMPs shall operate also with a single power supply of 3.3 Volt.
* rail-to-rail IO shall be supported by the OPAMPs.
* as the pulses generated by the SiPM module are very short (some few micro seconds in total) the bandwidth of the OPAMPs shall be very high (> 100 MHz).
* the used Schottky barrier rectifiers shall have as little forward voltage (VF) as possible (< ~300 mV).
* high quality multi-layer ceramic capacitors for smaller capacitors (<= 100 nF).
* high quality tantals for bigger capacitors (> 1 µF).

<img src="/Schematics/GammaSpectrometer.png" alt="" height="800" title="Schematics">

### Preamplifier

This circuit operates with 1/2 [TI OPA2354](/Datasheets/OP2354.pdf) in non-inverting amplifying mode. The gain can be configured with a trimmer `R2` in the range 1x - 14x, depending on which range of the gamma spectrum you are interested in. If you want the see the overall gamma spectrum created by this SiPM module (up to 8 MeV) then you would choose a gain factor of 1x. If you want to see the interesting low energy part of the gamma spectrum then you would choose some center position of the trimmer `R2`. The original pulse comming from the SiPM module can be measured at pin `MP_SIPM`. The amplitude of this pulse is equivalent to the energy [keV, MeV] of the gamma photon which caused this pulse. A screenshot taken with the oscilloscope can be seen in the following picture.

<img src="/Osci/osci01.png" alt="" height="400" title="Pulse from the SiPM module">

The amplified pulse is coupled out at pin `MP_AMP` and fead into the peak detection circuit. The following oscilloscope screenshot shows these pulses as an overlayed picture when having captured the different pulse amplitudes (gamma energies).

<img src="/Osci/osci02.png" alt="" height="400" title="Overlayed pulses after the preamplifier">

### Peak Detector (Sample & Hold)

This circuit implements an improved and performant peak detection circuit with one [TI OPA2354](/Datasheets/OP2354.pdf), two Schottky diodes [NXP PMEG4010BEA](/Datasheets/PMEG4010BEA_ENG_TDS.pdf) and one N-channel enhancement mode FET [Onsemi 2N7002](/Datasheets/NDS7002A-D.pdf).

It is used to buffer the source of the signal (`MP_AMP`) into the capacitor `C2`. As we can see the circuit is comprised of 2 OPAMPS. A high impedance load is offered by the OPAMP `U1B` to the source. While OPAMP `U2A` performs buffering action in between the load and capacitor `C2`. The voltage at the output side is the similar as the peak of the input signal stored in the capacitor `C2`. Its working is such that, as the input voltage becomes higher than the charge stored on the capacitor `C2`, it charges itself with the new higher value of input signal through the peak detection diode `D2`. However, for a smaller value of the input, the capacitor `C2` sticks to the previous higher value and the peak detection diode `D2` gets reverse biased.

The final piece of the circuit is `R5` and `D1`, which bootstrap the peak detection diode `D2`. Under that condition during the hold period, there can be no leakage through the diode `D2` resulting in a stable voltage at `D2`.

The charge of capacitor `C2` can be resetted/cleared after the hold period actively by the microcontroller at pin `RST`. This is done by discharging `C2` over the conducting FET and `R4`.

The buffered peak signal is coupled out at pin `SIG` and fead into the ADC- and pulse discriminator circuit. The following oscilloscope screenshot shows the buffered peak signal.

<img src="/Osci/osci03.png" alt="" height="400" title="Buffered peak signal">

### Pulse Diskriminator

This circuit is responsible for setting the trigger level for the microcontroller peak-interrupt. The circuit operates with 1/2 [TI OPA2354](/Datasheets/OP2354.pdf) in non-inverting comparator mode. The trigger level can be configured with a trimmer `R7` in the range ~0.07V - 0.63V. If the voltage of the source signal (`SIG`) is higher than the trigger level the output signal `INT` is set to 'High' (3.3V) as long the voltage of the source signal (`SIG`) doesn't go below the trigger level. Otherwise `INT` is set to 'Low' (0V). This means that during the peak sampling time no other peak-interrupt can be served by the microcontroller. The trigger level must be carefully adjusted to a minimum trigger level to also capture all small energies (peaks) but not too small to also capture noise (false peaks).

The interrupt signal is coupled out at pin `INT` and fead into the microcontroller.

### Analog Digital Converter (ADC)

The internal ADCs of many microcontrollers and as well for the ESP32 microcontroller have some pretty severe [Differencial Nonlinearity (DNL)](https://pico-adc.markomo.me/INL-DNL/#dnl) issues that result in some channels being much more sensitive (wider input range) than the rest.

That was the reason to use the external 12-bit ADC chip [Microchip MCP3201-B](/Datasheets/MCP3201.pdf) with SPI interface, which has a DNL and INL of only a maximum of +-1 LSB. The 12-bit resolution allows a maximum of 4092 energy channels, which is pretty good. The sampling rate of the ADC is about at 50 kHz which means one peak will be sampled in round about 20 µs, which is not very fast, but enough for this project. The 12-bit sample will be read out over SPI by the microcontroller.

### Microcontroller

I decided to take a NodeMCU ESP32 microcontroller board because of its performant cores, easy programming with Arduino IDE in C/C++, WIFI, small form factor, cheap price and a lot of experience from other projects. Following GPIOs are used:

  Signal      | ESP32  | Mode
  ------------|--------|----------------
  LED         | GPIO2  | GPIO output
  VSPI_CS0    | GPIO5  | SPI chip select
  VSPI_CLK    | GPIO18 | SPI clock
  VSPI_MISO   | GPIO19 | SPI data input
  RST         | GPIO21 | GPIO output
  INT         | GPIO22 | GPIO IRQ input
  
This module can be obtained at Ebay for about 5€. ![ESP32 NodeMCU](/Datasheets/ESP32S_pinout.jpg)

## Software
The Software can be found [here](/GammaSpectroMeter).

### Libraries

Following libraries are used by this project:
* [Arduino library for the MCP320x ADC family](https://github.com/labfruits/mcp320x/), a copy of the driver source code comes along with this project
* [WiFiManager](https://github.com/tzapu/WiFiManager)
* [ESPmDNS](https://github.com/espressif/arduino-esp32/tree/master/libraries/ESPmDNS)
* [ESPAsyncWebServer](https://github.com/me-no-dev/ESPAsyncWebServer)
* [ArduinoJson](https://github.com/bblanchon/ArduinoJson)
* [Arduino Time Library](https://github.com/PaulStoffregen/Time)

### Reset of Wifi Manager settings

To reset the Wifi settings (SSID, password) the code line `wm.resetSettings();` needs to be uncommented for one startup. Afterwards the line needs to be commented again and the device starts in Access Point mode (SSID = GammaConnectAP, IP = 192.168.4.1) showing the WifiManager frontendto the user. The new Wifi settings can then be entered.

### Initialization

The MCP320x driver is initialized for the MCP3201 variant with 800 kHz SPI clock because the chip is only powered with 3.3 Volt. Additional configurations for the MCP3201 driver is a reference voltage of 3.3 Volt, the usage of a chip select pin and MSB first transmission. The ISR pin is configured as input triggering the interrupt handler function `handleInterrupt()` on the rising edge.

At the end of initialization the asynchronous webserver is started (which provides the webpages below to the user) and the Multicast DNS protocol allows to connect to the device always with the same hostname with ending `.local` without using the IP address, e.g.:
* http://gamma.local/clear - reset and clear the actual measurement
* http://gamma.local/json - show the measured data in json format which can be downloaded for offline processing and showing
* http://gamma.local/spectrum - show the measured data graphically as a gamma spectrum

### Interrupt

The interrupt caused by gamma pulses is handled in function `handleInterrupt()`. At the beginning of the function at least 3 µs need to be waited until the output signal `SIG` has stabilized and reached its maximum peak. After that this maximum peak is sampled by triggering an ADC conversion. The ADC conversion takes about 20 µs after which the ADC value is read out and the channel corresponding to the sampled ADC value is increased by 1. Each sampled peak - depending on its individual height - will increase one of the 4096 channels. After more and more time the array of channels, which is in fact an array of gamma energies, represents finally a (non callibrated) gamma spectrum. At the end of the function (after the ADC conversion) the peak detection circuit is reset by asserting the signal `RST` for at least 1 µs.

### Data Export

The webserver provides all 4096 channel counters as a JSON formatted stream. This webpage can be displayed in any webbrowser by typing http://gamma.local/json. The displayed JSON stream can be downloaded as a JSON file for further offline processing (e.g. with the Python script). The JSON file contains in the header beside the 4096 channel counters also the elapsed time of the current measurement, the total number of events (peaks) in the current measurement and the average of counts (peaks) per minute. The following screenshot shows an example:

<img src="/Screenshots/screenshot01.png" alt="" width="1000" title="JSON stream">

### Visualization

The webserver provides also a visualization of the captured data. This webpage can be displayed in any webbrowser by typing http://gamma.local/spectrum. All channel counters are normalized by the elapsed time (unit: cpm, counts per minute) and are on the y-axis, whereas the channels [0 .. 4095] are on the x-axis. This gives you a gamma spectrum. An embedded javascript helps for visualization the spectrum in a Google line chart. The javascript produces also a second smoothed curve (red) which is generated by a kind of 2-way low pass filter. Beside this some useful information is shown in the heading of the webpage, e.g. the elapsed time of the current measurement, the total number of events (peaks) in the current measurement and the average of counts (peaks) per minute. The following screenshot shows an example:

<img src="/Screenshots/screenshot02.png" alt="" width="1000" title="Spectrum">
