[Setup]
AppName=Renomear Arquivos
AppVersion=1.0
DefaultDirName={userappdata}\Renomear Arquivos  ; Usando diretório do usuário
DefaultGroupName=Renomear Arquivos
OutputDir=.
OutputBaseFilename=Renomear_Arquivos_Instalador
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist/renomear_arquivos.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Renomear Arquivos"; Filename: "{app}\renomear_arquivos.exe"
Name: "{userdesktop}\Renomear Arquivos"; Filename: "{app}\renomear_arquivos.exe"

[Run]
Filename: "{app}\renomear_arquivos.exe"; Description: "Execute Renomear Arquivos"; Flags: nowait postinstall skipifsilent
