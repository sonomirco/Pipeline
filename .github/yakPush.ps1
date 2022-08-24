param($conString, $fileStored)
$fileShareName="yakfolder"
$folderPath="/"

## Get the storage account context 
$ctx = New-AzStorageContext -ConnectionString $conString
$fileShare=Get-AZStorageShare -Context $ctx -Name $fileShareName
echo $fileShare
## Upload the file

if (Test-Path -Path $fileStored) {
     try {
        $fileToStore=Get-ChildItem -path $fileStored -filter *.yak -file -ErrorAction silentlycontinue -recurse
        Set-AzStorageFileContent -Sharename $fileShare.Name -context $ctx -Source $fileToStore -Path $folderPath -Force
     }
     catch {
         throw $_.Exception.Message
     }
 }
# If the file already exists, show the message and do nothing.
 else {
     Write-Host "File [$fileShare] doesn't exist."
 }

## Disconnect from Azure Account  
Disconnect-AzAccount
