[Setup]
AppName=UniversityProject
AppVersion=1.0
DefaultDirName={autopf}\UniversityProject
DefaultGroupName=UniversityProject
OutputDir=output
OutputBaseFilename=UniversityProjectInstaller

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\UniversityProject"; Filename: "{app}\run.exe"
Name: "{commondesktop}\UniversityProject"; Filename: "{app}\run.exe"

[Run]
Filename: "{app}\run\run.exe"; Description: "Launch App"; Flags: nowait postinstall skipifsilent
