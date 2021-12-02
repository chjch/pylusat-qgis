# PyLUSAT for QGIS

The **Python for Land-use Suitability Analysis Tools** (PyLUSAT) is an 
open-source Python package dedicated for GIS-based land-use suitability 
modeling.
This QGIS plugin provides interfaces to all functions in PyLUSAT to 
allow easy access and better integration into the QGIS _processing framework_.

![pylusatq](screenshot/pylusatq_native.png)

For more information of PyLUSAT toolkit: https://github.com/chjch/pylusat

## Requirements
- _Recommended Windows edition_: Windows 7, Windows 10.
- *Recommended QGIS version*: 3.16 or higher.

## Installation

### 1. Set up <a href="https://pypi.org/project/pylusat/">PyLUSAT</a>

1. We suggest two ways to set up your computer for PyLUSAT.<br>
   **For beginners:** <ol type="a">
      <li> Visit <a href="https://github.com/chjch/pylusat-qgis">PyLUSAT 
      GitHub repository</a>. Click <b>Code</b>, and then <b>Download ZIP</b> 
      to download the <i>pylusat-qgis</i> repository.<br>
      <li>Copy `pylusat_installer.bat`, paste it under QGIS folder in your 
      system. 
      <li><b>Right Click</b> the copied <i>pylusat_installer.bat</i> to 
      <b>Run as administrator</b>.
   </ol><br>

   **OR, if you are familiar to work with terminals:**<br>
      Visit <a href="https://github.com/chjch/pylusat-qgis">PyLUSAT 
      GitHub repository</a>.
      Copy and paste the code in *pylusat_installer.bat* to your terminal 
      under the QGIS folder and run it.<br>

   >**Note**:<br>
   >The `pylusat_installer.bat` file helps you clean your environment and 
   >install proper pre-required packages. Noted that: <br> 1. we use `pipwin` 
   >instead of `pip` or `conda` considering the compatibility of QGIS and the
   >packages.<br> 2. we apply `pipwin refresh` to force a cache rebuild in case
   >any potential conflicts.<br> For more information about the PyLUSAT 
   >plugin, please visit https://github.com/chjch/pylusat.

2. In the pop-up window:
   <ol type="a">
      <li><b>Specify your root folder of QGIS</b>: 
      The same where you place the installer.
      <li><b>Is the QGIS a long term release [Y/N]</b>: 
      Refer to the version you installed. Type <b>Y</b> for long term release, 
      <b>N</b> for short term release.</li>
   </ol>
3. Press **Enter** key and wait for the installation to complete.

### 2. Install PyLUSAT plugin
1. Download **PyLUSAT plugin**
   from https://plugins.qgis.org/plugins/pylusatq/ 
2. Find **Plugins** on the top panel in your **QGIS Desktop**, 
   Click **Manage and install plugins...**
3. In **Install from ZIP** interface, 
   browse and select the PyLUSAT ZIP file you download. 
4. Click Install Plugin, once finished, restart QGIS.
   > **Note:**<br>
   > Once you click **Install Plugin**, you might see a pump-up window 
   > noticing "Couldn't load plugin pylusatq". 
   > Don't worry, the installation will succeed after you restart QGIS. 
5. Now you can find PyLUSAT tools in **Processing Toolbox** panel.