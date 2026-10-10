# Instala la CLI de Firebase (si falta) e inicia sesion.
$env:Path = "C:\Program Files\nodejs;$env:APPDATA\npm;$env:Path"
if (-not (Get-Command firebase -ErrorAction SilentlyContinue)) {
  npm install -g firebase-tools --no-fund --no-audit --loglevel=error
}
firebase login
