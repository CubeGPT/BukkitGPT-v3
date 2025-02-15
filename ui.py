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


# ---------- Functions ----------#
def open_config(args: dict) -> bool:
    """
    Opens the config file.

    Args:
        args (dict): A dictionary containing the necessary arguments.

    Returns:
        bool: Always True.
    """
    os.system("notepad config.yaml")

    return True


def save_apply_config(args: dict) -> bool:
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


def load_config(args: dict) -> bool:
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


def print_args(args: dict) -> bool:
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


# ---------- Generate Function ----------#
def generate(args: dict) -> bool:
    """
    Generates the plugin.

    Args:
        args (dict): A dictionary containing the necessary arguments.

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

    codes = core.askgpt(
        config.SYS_GEN.replace("%ARTIFACT_NAME%", artifact_name).replace(
            "%PKG_ID_LST%", pkg_id_path
        ),
        config.USR_GEN.replace("%DESCRIPTION", description),
        config.GENERATION_MODEL,
    )
    logger(f"codes: {codes}")

    core.response_to_action(codes)

    print("Code generated. Building now...")

    result = build.build_plugin(f"codes/{artifact_name}")

    target_dir = f"codes/{artifact_name}/target"
    jar_files = [f for f in os.listdir(target_dir) if f.endswith('.jar')]
    
    if jar_files:
        print(f"Build complete. Find your plugin at '{target_dir}/{jar_files[0]}'")
    else:
        error_msg = result
        print("Build failed. This is because the code LLM generated has syntax errors. Please try again or switch to a better LLM like o1 or r1. IT IS NOT A BUG OF BUKKITGPT.")

    return True


def edit(args: dict) -> bool:
    """
    Edits the plugin.

    Args:
        args (dict): A dictionary containing the arguments.

    Returns:
        bool: Always True.
    """
    # Get user inputs
    original_jar = args["OriginalJAR"].get()
    edit_request = args["EditRequest"].get()

    # Get the decompiled path
    decompiled_path = f"codes/decompiled/{original_jar.split('/')[-1].split('.')[0]}"

    # Decompile the jar
    core.decompile_jar(original_jar, decompiled_path)

    # Generate a buildable maven folder in the decompiled path
    os.makedirs(f"{decompiled_path}/src/main/java", exist_ok=True)

    # Delete decompiled_path/summary.txt
    summary_path = os.path.join(decompiled_path, "summary.txt")
    if os.path.exists(summary_path):
        os.remove(summary_path)

    # Move decompiled_path/* to decompiled_path/src/main/java
    for item in os.listdir(decompiled_path):
        if item != 'src':
            s = os.path.join(decompiled_path, item)
            d = os.path.join(decompiled_path, "src/main/java", item)
            if os.path.isdir(s):
                shutil.move(s, d)
            elif os.path.isfile(s):
                shutil.move(s, d)
    
    # Create empty pom.xml
    with open(f"{decompiled_path}/pom.xml", "w") as f:
        f.write("<!-- Replace with the pom.xml code -->")

    # Generate request
    code_text = core.code_to_text(decompiled_path)
    response = core.askgpt(
        config.SYS_EDIT,
        config.USR_EDIT.replace("ORIGINAL_CODE", code_text).replace("REQUEST", edit_request),
        config.GENERATION_MODEL,
        disable_json_mode=True
    )

    # Extract the response
    diffs = core.parse_edit_response(response)
    logger(f"[DEBUG] Extracted diffs: {diffs}")

    # Apply edit
    response = core.apply_diff_changes(diffs, decompiled_path)

    if response[0] == False:
        error_message = response[1]
        # TODO: Pass the error to the LLM and fix that
        print(f"The diff LLM generated is invalid. Please try again or switch to a better LLM like o1 or r1. IT IS NOT A BUG OF BUKKITGPT.")
    else:
        print("Edit complete. Recompiling...")
        result = build.build_plugin(decompiled_path)
        target_dir = f"{decompiled_path}/target"
        jar_files = [f for f in os.listdir(target_dir) if f.endswith('.jar')]
        
        if jar_files:
            print(f"Build complete. Find your plugin at '{target_dir}/{jar_files[0]}'")
        else:
            error_msg = result
            print("Build failed. This is because the code LLM generated has syntax errors. Please try again or switch to a better LLM like o1 or r1. IT IS NOT A BUG OF BUKKITGPT.")
        

    return True



# ---------- Main Program ----------#

root = CreateQGUI(title="BukkitGPT-v3",
                  tab_names=["Generate", "Edit", "Settings", "DevTools"]
                  )
error_msg = None

logger("Starting program.")

# Initialize Core
core.initialize()

print("BukkitGPT v3 beta console running")

# Banner
root.add_banner_tool(GitHub("https://github.com/CubeGPT/BukkitGPT-v3"))

# Generate Page
root.add_notebook_tool(
    InputBox(name="PluginName", default="ExamplePlugin", label_info="Plugin Name")
)
root.add_notebook_tool(
    InputBox(
        name="PluginDescription",
        default="Send msg 'hello' to every joined player.",
        label_info="Plugin Description",
    )
)

root.add_notebook_tool(
    RunButton(
        bind_func=generate,
        name="Generate",
        text="Generate Plugin",
        checked_text="Generating...",
        tab_index=0,
    )
)

# Edit Page #
root.add_notebook_tool(
    ChooseFileTextButton(
        name="OriginalJAR",
        label_info="Original JAR",
        tab_index=1
    )
)

root.add_notebook_tool(
    InputBox(
        name="EditRequest",
        default="Add a command to send a message to all players.",
        label_info="Edit Request",
        tab_index=1
    )
)

root.add_notebook_tool(
    RunButton(
        bind_func=edit,
        name="Edit",
        text="Edit Plugin",
        checked_text="Editing...",
        tab_index=1
    )
)

# Settings Page
root.add_notebook_tool(
    InputBox(
        name="API_KEY", 
        default=config.API_KEY, 
        label_info="API Key", 
        tab_index=2
    )
)
root.add_notebook_tool(
    InputBox(
        name="BASE_URL", 
        default=config.BASE_URL, 
        label_info="BASE URL", 
        tab_index=2
    )
)

config_buttons = HorizontalToolsCombine(
    [
        BaseButton(
            bind_func=save_apply_config,
            name="Save & Apply Config",
            text="Save & Apply",
            tab_index=2
        ),
        BaseButton(
            bind_func=load_config, 
            name="Load Config", 
            text="Load Config", 
            tab_index=2
        ),
        BaseButton(
            bind_func=open_config,
            name="Open Config",
            text="Open Full Config",
            tab_index=2
        ),
    ]
)
root.add_notebook_tool(config_buttons)

# DevTools Page
root.add_notebook_tool(
    Label(
        name="DevTool_DESCRIPTION",
        text="This is a testing page for developers. Ignore it if you are a normal user.",
        tab_index=3
    )
)
root.add_notebook_tool(
    Label(
        name="DevTool_CONFIG_API_KEY_DISPLAY",
        text=f"CONFIG.API_KEY = {config.API_KEY}",
        tab_index=3
    )
)
root.add_notebook_tool(
    Label(
        name="DevTools_CONFIG_BASE_URL_DISPLAY",
        text=f"CONFIG.BASE_URL = {config.BASE_URL}",
        tab_index=3
    )
)
root.add_notebook_tool(
    RunButton(
        bind_func=print_args, name="Print Args", text="Print Args", tab_index=3
    )
)
root.add_notebook_tool(
    RunButton(
        bind_func=raise_error, name="Raise Error", text="Raise Error", tab_index=3
    )
)

# Sidebar
root.set_navigation_about(
    author="CubeGPT Team",
    version=config.VERSION_NUMBER,
    github_url="https://github.com/CubeGPT/BukkitGPT-v3",
)


# Run
root.run()
