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

# Meniu pentru alegerea mediului virtual
Write-Host "Alege mediul virtual pe care vrei sa-l activezi:"
Write-Host "1. venv (varianta standard)"
Write-Host "2. venv_tf (pentru TensorFlow)"
$choice = Read-Host "Introdu optiunea (1 sau 2)"

# Creare mediu virtual
if ($choice -eq 1) {
    # Creeaza sau activeaza mediul virtual venv
    if (-not (Test-Path "venv")) {
        Write-Host "Creare mediu virtual 'venv'..."
        python -m venv venv
    } else {
        Write-Host "Mediu virtual 'venv' deja existent. Se trece la activare..."
    }
    # Activeaza mediul virtual venv
    . .\venv\Scripts\Activate.ps1
} elseif ($choice -eq 2) {
    # Creeaza sau activeaza mediul virtual venv_tf
    if (-not (Test-Path "venv_tf")) {
        Write-Host "Creare mediu virtual 'venv_tf' (TensorFlow)..."
        python -m venv venv_tf
    } else {
        Write-Host "Mediu virtual 'venv_tf' deja existent. Se trece la activare..."
    }
    # Activeaza mediul virtual venv_tf
    . .\venv_tf\Scripts\Activate.ps1
} else {
    Write-Host "Optiune invalida, scriptul se opreste."
    exit 1
}

# Actualizeaza pip
Write-Host "Actualizare pip la cea mai recenta versiune..."
python -m pip install --upgrade pip

# Instaleaza pachetele
Write-Host "Instalare pachete din requirements.txt..."
pip install -r requirements.txt

Write-Host "`nTotul este gata! Mediul virtual este activ si pachetele au fost instalate."
