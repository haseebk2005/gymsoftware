from PyInstaller.utils.hooks import collect_all

# Collect necessary files from django
datas, binaries, hiddenimports = collect_all('django')
