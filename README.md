# Gamma spectroscopy

## Introduction
Sooner or later your fingers will get itchy: once you deal with Geiger counters and with radioactivity, then you just want to try out at some time also gamma spectroscopy. But as a normal electronics hobbyist you usually have a lot of respect for that pure physics stuff with photomultipliers, scintillators and so forth. But once you have dared to cross this barrier, then you ask yourself why not started earlier.

My earlier Geiger counter projects using simple ionization tubes as detectors can only be used to count pulses caused by a passing gamma-ray and deriving the ionizing radiation dose. This project is doing the same, but an additional feature is the capability of measuring also the intensities of the pulses. The intensities of the pulses can be clearly assigned to gamma energies [unit keV]. Most radioactive sources produce gamma rays, which are of various energies and intensities. When these emissions are measured by this spectroscopy project, a gamma-ray energy spectrum can be produced afterwards from the collected data.

As we know now that a simple ionization tube as detector is not capable to measure gamma-ray energies, some other type of gamma-ray detector needs to come into game: a SiPM (Silicon Photo Multiplier) together with a scintillator.

## Scintillator

A scintillator is a material that is excited to glow in the visible range by incoming ionizing particles or radiation. I.e. it releases the absorbed energy in the form of light. A tight coupled photo multiplier is used to measure the sparkling of the emitted light. There exist various types of scintillators for different materials, wavelengths and sensitivities. The widely used NaI(Tl) (thallium-doped sodium iodide) inorganic crystal is also used in this project. The scintillation wavelength of the emitted photons fits to the used blue-sensitive photo multiplier. Incoming high energy radiation, i.e. in our case gamma photons, interact with the NaI(Tl) material and dissipate their kinetic energy to produce electron-hole pairs. The recombination of these electron-hole pairs leads to very short (few microseconds) visible light emissions. The presence of thallium significantly increases the light emission of the crystal and is referred to as an activator for the crystal.

![Scintillator With SiPM](/Images/image01.png)

The scintillator together with the photo multiplier must be housed in an absolutely light-tight housing so that the ambient light does not falsify the measurements. For this it is best to use some thin aluminum foil and black tape. The size of the used NaI(Tl) crystal is 10x10x30mm. In the following picture you see an example how the scintillator could look like.

![Scintillator NaI(Tl) Crystal](/Images/image02.png)
