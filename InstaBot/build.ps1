$exclude = @("venv", "InstaBot.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "InstaBot.zip" -Force