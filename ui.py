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
import build

#---------- Functions ----------#
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

#---------- Generate Function ----------#
def generate(args: dict):
    """
    Generates the plugin.

    Args:
        args (dict): A dictionary containing the arguments.

    Returns:
        bool: Always True.
    """
    global error_msg, pkg_id_path

    # Get user inputs
    name = args["PluginName"].get()
    description = args["PluginDescription"].get()
    
    artifact_name = name.replace(" ", "")
    package_id = f"org.cubegpt.{uuid.uuid4().hex[:8]}"

    pkg_id_path = ""
    for id in package_id.split("."):
        pkg_id_path += id + "/"

    logger(f"user_input -> name: {name}")
    logger(f"user_input -> description: {description}")
    logger(f"random_generate -> package_id: {package_id}")
    logger(f"str_path -> pkg_id_path: {pkg_id_path}")

    print("Generating plugin...")

    codes = core.askgpt(config.SYS_GEN.replace("%ARTIFACT_NAME%", artifact_name).replace("%PKG_ID_LST%", pkg_id_path), config.USR_GEN.replace("%DESCRIPTION", description), config.GENERATION_MODEL)
    logger(f"codes: {codes}")

    core.response_to_action(codes)

    print("Code generated. Building now...")

    result = build.build_plugin(artifact_name)
    if "BUILD SUCCESS" in result:
        print(f"Build complete. Find your plugin at 'codes/{artifact_name}/target/{artifact_name}.jar'")
    elif "Compilation failure":
        error_msg = result
        print("Build failed. To pass the error to ChatGPT && let it fix, jump to the Fixing page and click the Fix button.")
    else:
        print("Unknown error. Please check the logs && send the log to @BaimoQilin on discord.")


    return True

def fix(args: dict):
    """
    Fixes the error.

    Args:
        args (dict): A dictionary containing the arguments.

    Returns:
        bool: Always True.
    """
    artifact_name = args["PluginName"].get()

    print("Passing the error to ChatGPT...")

    files = [f"codes/{artifact_name}/src/main/java/{pkg_id_path}Main.java",
                f"codes/{artifact_name}/src/main/resources/plugin.yml",
                f"codes/{artifact_name}/src/main/resources/config.yml",
                f"codes/{artifact_name}/pom.xml"]

    ids = ["main_java",
            "plugin_yml",
            "config_yml",
            "pom_xml"]

    main_java = None
    plugin_yml = None
    config_yml = None
    pom_xml = None

    for file in files:
        with open(file, "r") as f:
            code = f.read()
            id = ids[files.index(file)]
            globals()[id] = code

    print("Generating...")
    codes = core.askgpt(config.SYS_FIX.replace("%ARTIFACT_NAME%", str(artifact_name)), config.USR_FIX.replace("%MAIN_JAVA%", str(main_java)).replace("%PLUGIN_YML%", str(plugin_yml)).replace("%CONFIG_YML%", str(config_yml)).replace("%POM_XML%", str(pom_xml)).replave("%PKG_ID_LST%", pkg_id_path).replace("%P_ERROR_MSG%", str(error_msg)), config.FIXING_MODEL)

    shutil.rmtree(f"codes/{artifact_name}")
    core.response_to_action(codes)

    print("Code generated. Building now...")

    result = build.build_plugin(artifact_name)

    if "BUILD SUCCESS" in result:
        print(f"Build complete. Find your plugin at 'codes/{artifact_name}/target/{artifact_name}.jar'")
    else:
        print("Build failed again. Please check the logs && send the log to @BaimoQilin on discord.")

    return True

#---------- Main Program ----------#

root = CreateQGUI(title="BukkitGPT-v3",
                  tab_names=["Generate", "Fixing", "Settings", "DevTools"]
                  )
error_msg = None

logger("Starting program.")

# Initialize Core
core.initialize()

print("BukkitGPT v3 beta console running")

# Banner
root.add_banner_tool(GitHub("https://github.com/CubeGPT/BukkitGPT-v3"))

# Generate Page
root.add_notebook_tool(InputBox(name="PluginName", default="ExamplePlugin", label_info="Plugin Name"))
root.add_notebook_tool(InputBox(name="PluginDescription", default="Send msg 'hello' to every joined player.", label_info="Plugin Description"))

root.add_notebook_tool(RunButton(bind_func=generate, name="Generate", text="Generate Plugin", checked_text="Generating...", tab_index=0))

# Fixing Page #
root.add_notebook_tool(Label(name="Fixing_DESCRIPTION", text="This is a fixing page. If the build fails, click the Fix button to fix the error in the LATEST build.", tab_index=1))
root.add_notebook_tool(RunButton(bind_func=fix, name="Fix", text="Fix", checked_text="Fixing...", tab_index=1))

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
                              github_url="https://github.com/CubeGPT/BukkitGPT-v3")



# Run
root.run()