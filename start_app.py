import platform, os, subprocess
from pathlib import Path

os_name = platform.system()
proj_dir = Path(os.path.dirname(os.path.realpath(__file__)))
os.environ['GIT_LOCAL_REPO'] = str(proj_dir)

if os_name == 'Windows':
    subprocess.run([os.path.join(proj_dir, "dist", "customer_onboarding_automation.exe")])
else:
    subprocess.run(["open", os.path.join(proj_dir, "dist", "customer_onboarding_automation.app")])
    