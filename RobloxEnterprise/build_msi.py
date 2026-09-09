import os
import subprocess
import sys

CANDLE_PATH = r"C:\Program Files (x86)\WiX Toolset v3.11\bin\candle.exe"
LIGHT_PATH = r"C:\Program Files (x86)\WiX Toolset v3.11\bin\light.exe"

def generate_wix_xml():
    wix_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://microsoft.com">
    <Product Id="*" Name="Roblox Enterprise Suite" Language="1033" Version="1.0.0.0" Manufacturer="Enterprise Bot Core" UpgradeCode="a9f2b778-bafe-4455-8c31-730b6a223b24">
        <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />
        <MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed." />
        <MediaTemplate EmbedCab="yes" />

        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="RobloxEnterpriseSuite" />
            </Directory>
            <Directory Id="DesktopFolder" Name="Desktop" />
        </Directory>

        <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
            <Component Id="MainExecutable" Guid="ef92b778-bafe-4455-8c31-730b6a223b24">
                <File Id="MainEXE" Source="dist\\main.exe" KeyPath="yes">
                    <Shortcut Id="DesktopShortcut" Directory="DesktopFolder" Name="Roblox Bot Suite" WorkingDirectory="INSTALLFOLDER" Icon="AppIcon.ico" IconIndex="0" Advertise="yes" />
                </File>
            </Component>
            <Component Id="NodeServer" Guid="25253892-bafe-4455-8c31-730b6a223b24">
                <File Id="ServerJS" Source="server.js" KeyPath="yes" />
            </Component>
            <Component Id="WebPanel" Guid="cdd6f492-bafe-4455-8c31-730b6a223b24">
                <File Id="IndexHTML" Source="index.html" KeyPath="yes" />
            </Component>
            <Component Id="LauncherBat" Guid="cba6f792-bafe-4455-8c31-730b6a223b24">
                <File Id="LaunchBAT" Source="launch_app.bat" KeyPath="yes" />
            </Component>
        </ComponentGroup>

        <Icon Id="AppIcon.ico" SourceFile="app_logo.ico" />

        <Feature Id="ProductFeature" Title="Roblox Enterprise Suite" Level="1">
            <ComponentGroupRef Id="ProductComponents" />
        </Feature>
    </Product>
</Wix>
"""
    with open("product_blueprint.wxs", "w", encoding="utf-8") as f:
        f.write(wix_xml)

def compile_msi_installer():
    if not os.path.exists(CANDLE_PATH) or not os.path.exists(LIGHT_PATH):
        print("❌ WiX Toolset path missing.")
        sys.exit(1)

    subprocess.run([CANDLE_PATH, "product_blueprint.wxs"], check=True)
    subprocess.run([LIGHT_PATH, "product_blueprint.wixobj", "-out", "RobloxEnterpriseSuiteSetup.msi"], check=True)

    if os.path.exists("product_blueprint.wxs"): os.remove("product_blueprint.wxs")
    if os.path.exists("product_blueprint.wixobj"): os.remove("product_blueprint.wixobj")
    if os.path.exists("product_blueprint.wixpdb"): os.remove("product_blueprint.wixpdb")
    print("🎉 Installer compiled: RobloxEnterpriseSuiteSetup.msi")

if __name__ == "__main__":
    generate_wix_xml()
    compile_msi_installer()
