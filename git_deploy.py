import subprocess
import time
import os

os.chdir(r'c:\Users\Professor\sistema_escolar')

print("Matando Python processes...")
os.system('taskkill /IM python.exe /F 2>nul')
time.sleep(1)

print("\n1. Git status:")
subprocess.run(['git', 'status'], check=False)

print("\n2. Git add all:")
subprocess.run(['git', 'add', '.'], check=False)

print("\n3. Git commit:")
subprocess.run(['git', 'commit', '-m', 'Fix: usar caminhos absolutos para database'], check=False)

print("\n4. Git push:")
subprocess.run(['git', 'push', 'origin', 'main'], check=False)

print("\n✅ PRONTO!")
print("Render irá redeploy automaticamente em ~2-3 minutos")
print("Visite: https://sistema-escolar-2q3l.onrender.com")
