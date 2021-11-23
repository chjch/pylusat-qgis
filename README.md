# PyLUSAT for QGIS

The Python for Land-use Suitability Analysis Tools (PyLUSAT) is an open-source
Python package dedicated for GIS-based land-use suitability modeling.
This QGIS plugin provides interfaces to all functions in PyLUSAT to allow
easy access and better integration into the QGIS _processing framework_.

![pylusatq](screenshot/pylusatq_native.png)


## Software Installation and Setup
## Get Started

1. Install PyLUSAT
2. Download plugin from 
3. Install plugin using zip file.


## System Requirements

- _Operating system_: 32-bit or 64-bit version of
  [Windows&reg;](https://tinyurl.com/4jcaub97).
- _Recommended Windows edition_: Windows 7, Windows 10.
- _Recommended memory size_: **8 GB** of [RAM](https://tinyurl.com/7s53ea9k).
- _System permission_: **Administrator Privilege** is needed to install QGIS.

> *QGIS 3.10.8 is a MUST**<br>
> To successfully load the _Processing Algorithms_ that the **GALUP** team
> developed, the QGIS **3.10.8** version is particularly **REQUIRED**. To avoid
> any potential conflicts, please first
> [perform an uninstallation](https://tinyurl.com/2bech66a)
> before moving forward on this instruction, if *another version* of QGIS is
> installed on your computer.

## Installation Steps

1. [Install QGIS](https://tinyurl.com/kwxcn6wd)
2. [Install PyLUSAT](https://tinyurl.com/27f4aepa)
3. [Load Processing Algorithms in QGIS](https://tinyurl.com/e6r2n7tm)

### 1. Install QGIS

1. Official website of QGIS [https://qgis.org/en/site/](https://qgis.org/en/site/).<br><br>

2. Click  **[Download Now](https://qgis.org/en/site/forusers/download.html)**. Go to **ALL RELEASES** where you can download
   **_Previous releases of QGIS are still available_**
   **_[here](https://qgis.org/downloads/)_**.
4. Download the version fit your setting. 
>**Version Compatibility**<br>
PyLUSAT can run in all versions of QGIS, including long-term releases and short term releases. 

### 2. Set up <a url="https://pypi.org/project/pylusat/">PyLUSAT</a> environment: Python for Land-Use Suitability Analysis Tools

1. Go to [https://github.com/chjch/pylusat-qgis](https://github.com/chjch/pylusat-qgis).
2. Click **Code**, and then click **Download ZIP** to download the _GALUP_
   repository.<br>
4. Copy `QGIS pylusat installer`, paste it under QGIS folder in your system. (Generally, you may find it under <code>C:\Program Files\QGIS</code> )

6.  **Right Click**  `install_pylusat.bat` to *Run as administrator*.
7. In the pop-up window:
   <ol type="a">
      <li><b>Specify your root folder of QGIS</b>: The same where you place the installer.
      <li><b>Is the QGIS a long term release [Y/N]</b>: Refer to the version you installed. Type <b>Y</b> for long term release, <b>N</b> for short term release.</li>
   </ol>
8. Press **Enter** key and wait for the installation to complete.<br>

### 3. Install PyLUSAT plug-in
1. Download <b>PyLUSAT plugin</b> from https://plugins.qgis.org/plugins/pylusatq/ 
2. In **QGIS Desktop** program, navigate to <b>Pugins</b> in top panel. Click <b>Manage and install plugins...</b>
3. In <b>Install from ZIP</b> interface, browse and select the PyLUSAT ZIP file you download. 
4. Click Install Plugin, once finished, <b>restart</b> QGIS.
   > **Loading error**<br>
   > Once you click Install Plugin, you might see a pump-up window noting "Couldent load plugin pylusatq". Don't worry, the installation will succeed after you restart QGIS. 
5. Now you can find PyLUSAT tools in <b>Processing Toolbox</b> panel.<br>

## Notes:
1. add rem to explain why pipwin https://plugins.qgis.org/plugins/pylusatq/
2. add rem to explain refresh 
3. link to https://github.com/chjch/pylusat