import sys
import uuid
import shutil

from log_writer import logger
import core
import config
import build

if __name__ == "__main__":
    main_java = None
    plugin_yml = None
    config_yml = None
    pom_xml = None

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

    result = build.build_plugin(artifact_name)

    if "BUILD SUCCESS" in result:
        print(
            f"Build complete. Find your plugin at 'codes/{artifact_name}/target/{artifact_name}.jar'"
        )
    elif "Compilation failure":
        print("Build failed. Passing the error to ChatGPT and let it to fix it?")
        fix = input("Y/n: ")
        if fix == "n":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Passing the error to ChatGPT...")

            files = [
                f"codes/{artifact_name}/src/main/java/{pkg_id_path}Main.java",
                f"codes/{artifact_name}/src/main/resources/plugin.yml",
                f"codes/{artifact_name}/src/main/resources/config.yml",
                f"codes/{artifact_name}/pom.xml",
            ]

            ids = ["main_java", "plugin_yml", "config_yml", "pom_xml"]

            for file in files:
                with open(file, "r") as f:
                    code = f.read()
                    id = ids[files.index(file)]
                    globals()[id] = code

            print("Generating...")
            codes = core.askgpt(
                config.SYS_FIX.replace("%ARTIFACT_NAME%", artifact_name),
                config.USR_FIX.replace("%MAIN_JAVA%", main_java)
                .replace("%PLUGIN_YML%", plugin_yml)
                .replace("%CONFIG_YML%", config_yml)
                .replace("%POM_XML%", pom_xml)
                .replace("%P_ERROR_MSG%", result),
                config.FIXING_MODEL,
            )

            shutil.rmtree(f"codes/{artifact_name}")
            core.response_to_action(codes)

            print("Code generated. Building now...")

            result = build.build_plugin(artifact_name)

        if "BUILD SUCCESS" in result:
            print(
                f"Build complete. Find your plugin at 'codes/{artifact_name}/target/{artifact_name}.jar'"
            )
        else:
            print(
                "Build failed. Please check the logs && send the log to @BaimoQilin on discord."
            )
            print("Exiting...")
            sys.exit(0)

    else:
        print(
            "Unknown error. Please check the logs && send the log to @BaimoQilin on discord."
        )
        print("Exiting...")
        sys.exit(0)


else:
    print(
        "Error: Please run console.py as the main program instead of importing it from another program."
    )
