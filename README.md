# PyLUSAT for QGIS

The <b>Python for Land-use Suitability Analysis Tools (PyLUSAT)</b> is an open-source
Python package dedicated for GIS-based land-use suitability modeling.
This QGIS plugin provides interfaces to all functions in PyLUSAT to allow
easy access and better integration into the QGIS _processing framework_.

![pylusatq](screenshot/pylusatq_native.png)

For more information of PyLUSAT toolkit:
https://github.com/chjch/pylusat

# Software Installation and Setup

## System Requirements

- _Operating system_: 32-bit or 64-bit version of
  [Windows&reg;](https://tinyurl.com/4jcaub97).
- _Recommended Windows edition_: Windows 7, Windows 10.
- _Recommended memory size_: **8 GB** of [RAM](https://tinyurl.com/7s53ea9k).
- _System permission_: **Administrator Privilege** is needed to install QGIS.

## Installation Steps

### 1. Install QGIS

1. Download QGIS with any version from official website of QGIS [https://qgis.org/en/site/](https://qgis.org/en/site/).<br><br>
2. Click  **[Download Now](https://qgis.org/en/site/forusers/download.html)**. Go to **ALL RELEASES** where you can download
   **_Previous releases of QGIS are still available_**
   **_[here](https://qgis.org/downloads/)_**.
3. Download and install the version that fit your setting. 
   >**Version Compatibility**<br>
PyLUSAT can run in all versions of QGIS, including long-term releases and short term releases. 

### 2. Set up <a url="https://pypi.org/project/pylusat/">PyLUSAT</a> environment

1. We suggest two ways to set up your computer for PyLUSAT.

   **For beginners:**<br>
a. Visit [https://github.com/chjch/pylusat-qgis](https://github.com/chjch/pylusat-qgis)<br>
b. Click **Code**, and then click **Download ZIP** to download the _pylusat-qgis_
   repository.<br>
c. Copy `pylusat_installer.bat`, paste it under QGIS folder in your system. 
   >Generally, you may find it under <code>C:\Program Files\QGIS</code> <br>

   d. <b>Right Click</b>  `pylusat_installer.bat `to *Run as administrator*.<br>

   ***OR, if you are familiar to work with terminals:**<br>
a. Visit [https://github.com/chjch/pylusat-qgis](https://github.com/chjch/pylusat-qgis)<br>
b. Copy and paste the code in `pylusat_installer.bat` to your terminal under the QGIS folder. Run it.
   > The `pylusat_installer.bat` file helps you clean your environment and install proper pre-required packages. Noted that: <br> 1. we use `pipwin` instead of `pip` or `conda` considering the compatibility of QGIS and the packages.<br> 2. we apply `pipwin refresh` to force a cache rebuild in case any potential conflicts.<br> For more information about the PyLUSAT plugin, please visit https://github.com/chjch/pylusat.

2. In the pop-up window:
   <ol type="a">
      <li><b>Specify your root folder of QGIS</b>: The same where you place the installer.
      <li><b>Is the QGIS a long term release [Y/N]</b>: Refer to the version you installed. Type <b>Y</b> for long term release, <b>N</b> for short term release.</li>
   </ol>
8. Press <b>Enter</b> key and wait for the installation to complete.<br>

### 3. Install PyLUSAT plug-in
1. Download <b>PyLUSAT plugin</b> from https://plugins.qgis.org/plugins/pylusatq/ 
2. In **QGIS Desktop** program, navigate to <b>Pugins</b> in top panel. Click <b>Manage and install plugins...</b>
3. In <b>Install from ZIP</b> interface, browse and select the PyLUSAT ZIP file you download. 
4. Click Install Plugin, once finished, <b>restart</b> QGIS.
   > **Loading Error**<br>
   > Once you click Install Plugin, you might see a pump-up window noting "Couldent load plugin pylusatq". Don't worry, the installation will succeed after you restart QGIS. 
5. Now you can find PyLUSAT tools in <b>Processing Toolbox</b> panel.<br>