import os
import subprocess
import time
"""
curdir is datenManagement/python/sphinx-doc

build script for writing apidoc to folder ./api/
from packages one folder below curdir: ../{package}
"""

package = "autobasedoc"

build_str = f"sphinx-apidoc -fEe ../{package} -o api"

p = subprocess.Popen(
    build_str,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
retval = p.wait()
if retval == 0:
    time.sleep(1.0)
else:
    print("system call failed: ", p.stdout.read())
