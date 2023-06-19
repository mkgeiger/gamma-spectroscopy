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

This circuit operates with 1/2 [TI OPA2354](/Datasheets/OP2354.pdf) in non-inverting mode. The gain can be configured with a trimmer `R2` in the range 1x - 14x, depending on which range of the gamma spectrum you are interested in. If you want the see the overall gamma spectrum created by this SiPM module (up to 8 MeV) then you would choose a gain factor of 1x. If you want to see the interesting low energy part of the gamma spectrum then you would choose some center position of the trimmer `R2`. The original pulse comming from the SiPM module can be measured at pin `MP_SIPM`. The amplitude of this pulse is equivalent to the energy [keV, MeV] of the gamma photon which caused this pulse. A screenshot taken with the oscilloscope can be seen in the following picture.

<img src="/Osci/osci01.png" alt="" height="400" title="Pulse from the SiPM module">

The amplified pulse is coupled out at pin `MP_AMP`. The following oscilloscope screenshot shows these pulses as an overlayed picture when having captured the different pulse amplitudes (gamma energies).

<img src="/Osci/osci02.png" alt="" height="400" title="Overlayed pulses after the preamplifier">
