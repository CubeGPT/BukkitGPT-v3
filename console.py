import sys
import uuid

from log_writer import logger
import core
import config
import build

if __name__ == "__main__":
    core.initialize()

    print("BukkitGPT v3 beta console running")

    # Get user inputs
    name = input("Enter the plugin name: ")
    description = input("Enter the plugin description: ")
    
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
        print("Build failed. Passing the error to ChatGPT and let it to fix it?")
        fix = input("Y/n: ")
        if fix == "n":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Fixing is a uncompleted feature.")
            print("Restart the program and retype the name & description, etc. to try again.")
            print("Exiting...")
            sys.exit(0)
    else:
        print("Unknown error. Please check the logs && send the log to @BaimoQilin on discord.")
        print("Exiting...")
        sys.exit(0)


else:
    print("Error: Please run console.py as the main program instead of importing it from another program.")