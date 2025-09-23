import subprocess

compile = [
    'pyinstaller',
    '--onefile',
    '--clean',
    '--noconfirm',
    '--windowed',
    '--icon=app.ico',
    '--add-data', 'instance_types.txt:.',
    '--name', 'customer_onboarding_automation',
    'setup.py'
]

subprocess.run(compile)

# Execute Application
print('\nStarting Application ...')

try:
    subprocess.run(["python3", "start_app.py"], check=True)
except (FileNotFoundError):
    print(f"python3 not found, trying with 'python'...")
    subprocess.run(["python", "start_app.py"], check=True)
