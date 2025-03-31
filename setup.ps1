# setup.ps1

# Verifica daca Python este instalat
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python nu este instalat sau nu este in PATH. Instaleaza-l de la https://www.python.org/downloads/"
    exit 1
}

# Verifica daca requirements.txt exista
if (-not (Test-Path "requirements.txt")) {
    Write-Error "Fisierul requirements.txt nu a fost gasit in directorul curent."
    exit 1
}

# Creeaza mediu virtual daca nu exista
if (-not (Test-Path "venv")) {
    Write-Host "Creare mediu virtual..."
    python -m venv venv
} else {
    Write-Host "Mediu virtual deja existent. Se trece la activare..."
}

# Activeaza mediul virtual
Write-Host "Activare mediu virtual..."
. .\venv\Scripts\Activate.ps1

# Actualizeaza pip
Write-Host "Actualizare pip la cea mai recenta versiune..."
python -m pip install --upgrade pip

# Instaleaza pachetele
Write-Host "Instalare pachete din requirements.txt..."
pip install -r requirements.txt

Write-Host "`nTotul este gata! Mediul virtual este activ si pachetele au fost instalate."
