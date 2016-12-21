##    Copyright (C) 2016 Canopus GeoInformatics Ltd.
##
##    This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License along
##    with this program; if not, If not, see <http://www.gnu.org/licenses/>.

import _winreg
import sys
import os
from os import path


def ArcpyInstallDir():

    '''
    Function used to determine the installation path of ArcGIS Desktop. Access
    registry keys based on the appropriate registry view (32 or 64). Bitness is

    determined by the running python process the script is executing.
    INPUT:
    None
 
    OUTPUT:
    Install Path: Returns the "InstallDir" registry key value of the to the
                  installed ESRI ArcGIS product. The search order is Desktop,
                  Engine, Server

    NOTES:
        Keys to check:
        
        HLKM/SOFTWARE/ESRI/ArcGIS 

        HLKM/SOFTWARE/ESRI/ArcGIS 'RealVersion' - will give the version, that we can use
        to build the registry key for the various ArcGIS products

        HKLM/SOFTWARE/ESRI/DesktopX.Y 'InstallDir'. Where X.Y is the version
        HKLM/SOFTWARE/ESRI/EngineX.Y 'InstallDir'. Where X.Y is the version
        HKLM/SOFTWARE/ESRI/ServerX.Y 'InstallDir'. Where X.Y is the version
     '''

    # https://blogs.msdn.microsoft.com/david.wang/2006/03/27/howto-detect-process-bitness/ 
    proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower() #processor architecture, WOW64 reports x86.
          
    # Use the bitness of the python process we are running to determine the registry view we should access.
    # this should keep from trying to use a 64bit python interpreter with 32bit arcpy libraries(dll's) and vise-versa
    if proc_arch == 'x86': 
        keyMask = _winreg.KEY_READ | _winreg.KEY_WOW64_32KEY #32bit registry view
    elif proc_arch == 'amd64':
        keyMask = _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY #64bit registry view
    else:
        raise Exception("Unhandled arch: %s" % proc_arch)
    
    try:
        # lets operate on the registry using the proper registry view for the current process  
        # HKLM/SOFTWARE/Wow6432Node/ESRI (64bit registry) = HKLM/SOFTWARE/ESRI (32bit view) 
        # HKLM/SOFTWARE/ESRI (64bit registry) = HKLM/SOFTWARE/ESRI (64bit view)
        
        # connect to the registry
        aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
      
        # get the root reg key object for the installed ESRI products using a 32bit
        # or 64bit registry view
        esriKeyName = 'SOFTWARE\\ESRI'
        esriKey = _winreg.OpenKey(aReg, esriKeyName, 0, keyMask) 

        # get the registry key for the suite of ESRI ArcGIS installed products
        # HKLM/SOFTWARE/ESRI/ArcGIS'  
        arcKey = _winreg.OpenKey(esriKey, 'ArcGIS', 0)

        # parse the major.minor version from the value, assuming the format follows
        # semantic version(major.minor.patch) scheme 
        arcVersionValue = path.splitext(_winreg.QueryValueEx(arcKey, "RealVersion")[0])[0]
 
        # build a list of product keys we will look for
        arcDesktopKeyName = "Desktop{0}".format(arcVersionValue)
        arcEngineKeyName = "Engine{0}".format(arcVersionValue)
        arcServerKeyName = "Server{0}".format(arcVersionValue)
        
        for keyName in [arcDesktopKeyName,arcEngineKeyName,arcServerKeyName]:
            # get the installDir value for current version of ArcGIS desktop products installed
            # HKLM/SOFTWARE/ESRI/DesktopX.Y
            # HKLM/SOFTWARE/ESRI/EngineX.Y
            # HKLM/SOFTWARE/ESRI/ServerX.Y
            try:
                prodKey = _winreg.OpenKey(esriKey, keyName, 0)
                break
            except WindowsError:
                prodKey = None
                continue
        # get the Install directory for the first ArcGIS product found in the order (desktop,engine,server)
        install_dir = _winreg.QueryValueEx(prodKey, "InstallDir")[0]
        return install_dir
    except WindowsError:
        raise Exception("Could not locate the ArcGIS product install directory on this machine")

def Set_CondaPath(envName):
    '''
    Adds path to necessary to ArcGIS python sys.path to support importing modules installed
    in a specific conda environment.
    '''
    pass

def Set_ArcpyPath():
    '''
    Adds paths necessary to sys.path in the current python environment to support
    importing the ESRI arcpy module. 

    INPUT:
    None
 
    OUTPUT:
    None
    '''
 
    install_dir = ArcpyInstallDir()

    #can only be used on windows platform OS(32 or 64)bit, not a issue for desktop, server
    # may be used in a non windows environment like linux
    if sys.platform == 'win32':
        arcpy_dir = path.join(install_dir, "arcpy")
        # Check for the arcpy directory.
        if not path.exists(arcpy_dir):
            raise ImportError("Could not find //arcpy directory in {0}".format(install_dir))

        bin_dir = path.join(install_dir, "bin64") #this exists when arcpy dll's are 64bit
        if not path.exists(bin_dir):
            bin_dir = path.join(install_dir, "bin")

        # Check for the bin64 or bin directory
        if not path.exists(bin_dir):
            raise ImportError("Could not find //bin directory in {0}".format(install_dir))

        # Check for the scripts directory. 
        scripts_dir = path.join(install_dir, "ArcToolbox", "Scripts")

        if not path.exists(scripts_dir):
            raise ImportError("Could not find //ArcToolbox//Scripts directory in {0}".format(install_dir))
     
        sys.path.extend([arcpy_dir, bin_dir, scripts_dir])
    else:
        raise ImportError("Module can only be used on Win32 platform")

#add the paths when the module is imported
Set_ArcpyPath()
