Import-Module ActiveDirectory
$Domain = "nullbyte.exe"
$OUs = @("dev", "svc", "mgmt", "ext")

foreach ($OUName in $OUs) {
    try {
        New-ADOrganizationalUnit -Name $OUName -Path "DC=nullbyte,DC=exe"
        Write-Host "Organizational Unit '$OUName' created successfully."
    } catch {
        Write-Host "Failed to create OU '$OUName'. Error: $_"
    }
}

$csvPath = Join-Path -Path (Get-Location) -ChildPath "users.csv"
$users = Import-Csv -Path $csvPath

foreach ($user in $users) {
    $OUPath = "OU=$($user.OU),DC=nullbyte,DC=exe"
    $Password = ConvertTo-SecureString $user.Password -AsPlainText -Force

    try {
        New-ADUser -Name "$($user.FirstName) $($user.LastName)" `
                   -GivenName $user.FirstName `
                   -Surname $user.LastName `
                   -SamAccountName $user.UserName `
                   -UserPrincipalName "$($user.UserName)@nullbyte.exe" `
                   -Path $OUPath `
                   -AccountPassword $Password `
                   -Enabled $true
        Write-Host "User '$($user.UserName)' created successfully in OU '$($user.OU)'."
    } catch {
        Write-Host "Failed to create user '$($user.UserName)'. Error: $_"
    }
}

