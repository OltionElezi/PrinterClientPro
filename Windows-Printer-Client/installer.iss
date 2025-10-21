; Print Client Pro - Inno Setup Installer Script
; Professional Windows Installer for Distribution

#define MyAppName "Print Client Pro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Print Client Pro"
#define MyAppURL "https://www.printclientpro.com"
#define MyAppExeName "PrintClientPro.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{8F9D6C3A-2E4B-4A1D-9F3E-5C8B7A2D4E6F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installer_output
OutputBaseFilename=PrintClientPro_Setup_v{#MyAppVersion}
SetupIconFile=printer_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Sign the installer (requires code signing certificate)
; SignTool=signtool
; SignedUninstaller=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Start {#MyAppName} automatically when Windows starts"; GroupDescription: "Auto-start:"; Flags: checked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startupicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
var
  ConfigPage: TInputQueryWizardPage;
  ServerURLEdit: TEdit;
  NIPTEdit: TEdit;
  UsernameEdit: TEdit;
  SessionIDEdit: TEdit;

procedure InitializeWizard;
begin
  { Create custom configuration page }
  ConfigPage := CreateInputQueryPage(wpSelectTasks,
    'Initial Configuration',
    'Please enter your Print Client Pro configuration',
    'These settings will be saved and used when the application starts. You can change them later from the application settings.');

  { Add configuration fields }
  ConfigPage.Add('Socket Server URL:', False);
  ConfigPage.Add('NIPT (Company ID):', False);
  ConfigPage.Add('Username:', False);
  ConfigPage.Add('Session ID:', False);

  { Set default values }
  ConfigPage.Values[0] := 'http://127.0.0.1:5001';
  ConfigPage.Values[1] := '';
  ConfigPage.Values[2] := '';
  ConfigPage.Values[3] := '';
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;

  { Validate configuration page }
  if CurPageID = ConfigPage.ID then
  begin
    if Trim(ConfigPage.Values[0]) = '' then
    begin
      MsgBox('Please enter the Socket Server URL.', mbError, MB_OK);
      Result := False;
      Exit;
    end;

    if Trim(ConfigPage.Values[1]) = '' then
    begin
      MsgBox('Please enter your NIPT (Company ID).', mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  EnvContent: AnsiString;
  EnvFilePath: String;
begin
  if CurStep = ssPostInstall then
  begin
    { Create .env file with configuration }
    EnvFilePath := ExpandConstant('{app}\.env');

    EnvContent :=
      '# Print Client Pro Configuration' + #13#10 +
      '# Socket Server Settings' + #13#10 +
      'SOCKET_SERVER_URL=' + ConfigPage.Values[0] + #13#10 +
      #13#10 +
      '# Client Identification' + #13#10 +
      'NIPT=' + ConfigPage.Values[1] + #13#10 +
      'USERNAME=' + ConfigPage.Values[2] + #13#10 +
      'SESSION_ID=' + ConfigPage.Values[3] + #13#10 +
      #13#10 +
      '# Reconnection Settings' + #13#10 +
      'RECONNECT_DELAY=5' + #13#10 +
      'MAX_RECONNECT_ATTEMPTS=0' + #13#10;

    SaveStringToFile(EnvFilePath, EnvContent, False);

    { Show success message }
    MsgBox('Configuration saved successfully!' + #13#10 + #13#10 +
           'Print Client Pro is now configured and ready to use.', mbInformation, MB_OK);
  end;
end;

[UninstallDelete]
Type: files; Name: "{app}\.env"
Type: files; Name: "{app}\printer_client_gui.log"
Type: files; Name: "{app}\printer_settings.json"
