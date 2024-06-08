from cx_Freeze import setup, Executable

import config

files = [
    "config.yaml",
    "LICENSE",
    "README.md",
    "requirements.txt",
    "logs"
    # More files can be added here
]

setup(name='CubeAgents', # Change this to the name of your app
      version=config.VERSION_NUMBER,
      maintainer="CubeGPT Team",
      maintainer_email="admin@cubegpt.org",
      url="https://github.com/CubeGPT/CubeAgents",
      license="Apache License 2.0",
      description='A app-template for CubeGPT projects.',
      executables=[Executable('ui.py', base="gui")],
      options={
          "build_exe": {
              "include_files": files,
          }
      })