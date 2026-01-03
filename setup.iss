; Script de instalación para Sistema de Gestión Académica CEDUC
; Requiere Inno Setup: https://jrsoftware.org/isdl.php

[Setup]
AppName=Sistema de Gestión Académica CEDUC
AppVersion=1.0.0
AppPublisher=CEDUC - Centro Educacional
DefaultDirName={autopf}\CEDUC
DefaultGroupName=CEDUC
OutputDir=installer
OutputBaseFilename=CEDUC_Sistema_Academico_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
; Incluir todos los archivos de la carpeta build/windows
Source: "build\windows\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
; Crear acceso directo en el menú de inicio
Name: "{group}\Sistema Académico CEDUC"; Filename: "{app}\main_flet_moderno.exe"
; Crear acceso directo en el escritorio
Name: "{autodesktop}\Sistema Académico CEDUC"; Filename: "{app}\main_flet_moderno.exe"

[Run]
; Opción para ejecutar la aplicación después de la instalación
Filename: "{app}\main_flet_moderno.exe"; Description: "Ejecutar Sistema Académico CEDUC"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
; Limpiar archivos generados (reportes, logs, etc.)
Type: filesandordirs; Name: "{app}\reportes"
