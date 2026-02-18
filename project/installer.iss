[Setup]
AppName=UniversityProject
AppVersion=1.0
DefaultDirName={pf}\UniversityProject
DefaultGroupName=UniversityProject
OutputDir=output
OutputBaseFilename=UniversityProjectInstaller

[Files]
Source: "dist\run.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\UniversityProject"; Filename: "{app}\run.exe"
Name: "{commondesktop}\UniversityProject"; Filename: "{app}\run.exe"

[Run]
Filename: "{app}\run.exe"; Description: "Launch App"; Flags: nowait postinstall skipifsilent
