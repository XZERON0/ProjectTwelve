[Setup]
AppName=UniversityProject
AppVersion=1.0
DefaultDirName={autopf}\UniversityProject
DefaultGroupName=UniversityProject
OutputDir=output
OutputBaseFilename=UniversityProjectInstaller
UninstallFilesDir={app}
UninstallDisplayIcon={app}\run.exe
PrivilegesRequired=admin

[Files]
Source: "dist\run.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\UniversityProject"; Filename: "{app}\run.exe"
Name: "{commondesktop}\UniversityProject"; Filename: "{app}\run.exe"

[Run]
Filename: "{app}\run.exe"; Description: "Запустить UniversityProject"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Убиваем процесс перед удалением
Filename: "{cmd}"; Parameters: "/c taskkill /f /im run.exe"; Flags: runhidden waituntilterminated

[UninstallDelete]
; Удаляем всё что создала программа
Type: files; Name: "{app}\*.db"
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.sqlite3"
Type: filesandordirs; Name: "{app}\static"
Type: filesandordirs; Name: "{app}\media"
Type: filesandordirs; Name: "{app}\__pycache__"

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Удаляем папку программы если осталась
    if DirExists(ExpandConstant('{app}')) then
      DelTree(ExpandConstant('{app}'), True, True, True);
  end;
end;