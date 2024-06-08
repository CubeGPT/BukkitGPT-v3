from cube_qgui.__init__ import CreateQGUI
from cube_qgui.banner_tools import *
from cube_qgui.notebook_tools import *
from playwright.sync_api import Playwright, sync_playwright
import os
import shutil
import uuid

from log_writer import logger
import config
import core

def open_config(args: dict):
    """
    Opens the config file.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    os.system("notepad config.yaml")

    return True

def save_apply_config(args: dict):
    """
    Saves and applies the configuration.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    keys = ["API_KEY", "BASE_URL"]

    for key in keys:
        value = args[key].get()

        if key == "ADVANCED_MODE":
            value = True if value == 1 else False
        else:
            pass

        config.edit_config(key, value)

    config.load_config()

    args["DevTool_CONFIG_API_KEY_DISPLAY"].set(f"CONFIG.API_KEY = {config.API_KEY}")
    args["DevTools_CONFIG_BASE_URL_DISPLAY"].set(f"CONFIG.BASE_URL = {config.BASE_URL}")

    return True

def load_config(args: dict):
    """
    Loads the configuration.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    config.load_config()

    args["API_KEY"].set(config.API_KEY)
    args["BASE_URL"].set(config.BASE_URL)

    return True

def print_args(args: dict):
    """
    Prints the arguments.

    Args:
        args (dict): A dictionary containing the arguments.

    Returns:
        bool: Always True.
    """
    for arg, v_fun in args.items():
        print(f"Name: {arg}, Value: {v_fun.get()}")

    return True

def raise_error(args: dict):
    """
    Raises an error.

    Args:
        args (dict): A dictionary containing the arguments.
    """
    raise Exception("This is a test error.")

root = CreateQGUI(title="CubeAgents",
                  tab_names=["Generate", "Settings", "DevTools"]
                  )

logger("Starting program.")

# Initialize Core
core.initialize()

# Banner
root.add_banner_tool(GitHub("https://github.com/CubeGPT/CubeAgents"))

# Generate Page
# Codes here.

# More pages here.

# Settings Page
root.add_notebook_tool(InputBox(name="API_KEY", default=config.API_KEY, label_info="API Key", tab_index=2))
root.add_notebook_tool(InputBox(name="BASE_URL", default=config.BASE_URL, label_info="BASE URL", tab_index=2))

config_buttons = HorizontalToolsCombine([
     BaseButton(bind_func=save_apply_config, name="Save & Apply Config", text="Save & Apply", tab_index=2),
     BaseButton(bind_func=load_config, name="Load Config", text="Load Config", tab_index=2),
     BaseButton(bind_func=open_config, name="Open Config", text="Open Full Config", tab_index=2)
])
root.add_notebook_tool(config_buttons)

# DevTools Page
root.add_notebook_tool(Label(name="DevTool_DESCRIPTION", text="This is a testing page for developers. Ignore it if you are a normal user.", tab_index=3))
root.add_notebook_tool(Label(name="DevTool_CONFIG_API_KEY_DISPLAY", text=f"CONFIG.API_KEY = {config.API_KEY}", tab_index=3))
root.add_notebook_tool(Label(name="DevTools_CONFIG_BASE_URL_DISPLAY", text=f"CONFIG.BASE_URL = {config.BASE_URL}", tab_index=3))
root.add_notebook_tool(RunButton(bind_func=print_args, name="Print Args", text="Print Args", tab_index=3))
root.add_notebook_tool(RunButton(bind_func=raise_error, name="Raise Error", text="Raise Error", tab_index=3))

# Sidebar
root.set_navigation_about(author="CubeGPT Team",
                              version=config.VERSION_NUMBER,
                              github_url="https://github.com/CubeGPT/CubeAgents")



# Run
root.run()