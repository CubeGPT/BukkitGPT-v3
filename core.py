from openai import OpenAI, APIConnectionError, AuthenticationError
import chardet
import sys
import json
import locale
import os
import requests
import subprocess
import re
import shutil

from diff import apply_patch
from log_writer import logger
import config


def initialize() -> None:
    """
    Initializes the software.

    This function logs the software launch, including the version number and platform.

    Args:
        None

    Returns:
        None
    """
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    logger(f"Launch. Software version {config.VERSION_NUMBER}, platform {sys.platform}")


def askgpt(
        system_prompt: str,
        user_prompt: str,
        model_name: str,
        disable_json_mode: bool = False,
        image_url: str = None
    ) -> str:
    """
    Interacts with the LLM using the specified prompts.

    Args:
        system_prompt (str): The system prompt.
        user_prompt (str): The user prompt.
        model_name (str): The model name to use.
        disable_json_mode (bool): Whether to disable JSON mode.

    Returns:
        str: The response from the LLM.
    """
    if image_url is not None and config.USE_DIFFERENT_APIKEY_FOR_VISION_MODEL:
        logger("Using different API key for vision model.")
        client = OpenAI(api_key=config.VISION_API_KEY, base_url=config.VISION_BASE_URL)
    else:
        client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)

    logger("Initialized the OpenAI client.")

    # Define the messages for the conversation
    if image_url is not None:
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            },
        ]
    elif config.GENERATION_MODEL == "o1-preview" or config.GENERATION_MODEL == "o1-mini":
        messages = [
            {"role": "user", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    logger(f"askgpt: system {system_prompt}")
    logger(f"askgpt: user {user_prompt}")

    # Create a chat completion
    try:
        response = client.chat.completions.create(
            model=model_name, messages=messages,
            max_tokens=10000,
            extra_headers={
                "HTTP-Referer": "https://cubegpt.org",
                "X-Title": "CubeGPT"
            }
        )
    except APIConnectionError as e:
        raise Exception("Failed to connect to your LLM provider. Please check your configuration (make sure the BASE_URL ends with /v1) and internet connection. IT IS NOT A BUG OF BUKKITGPT.")
    except AuthenticationError as e:
        raise Exception("Your API key is invalid. Please check your configuration. IT IS NOT A BUG OF BUKKITGPT.")
    except Exception as e:
        raise e

    logger(f"askgpt: response {response}")

    if "Too many requests" in str(response):
        logger("Too many requests. Please try again later.")
        raise Exception("Your LLM provider has rate limited you. Please try again later. IT IS NOT A BUG OF BUKKITGPT.")

    # Extract the assistant's reply
    try:
        assistant_reply = response.choices[0].message.content
        logger(f"askgpt: extracted reply {assistant_reply}")
    except Exception as e:
        logger(f"askgpt: error extracting reply {e}")
        raise Exception("Your LLM didn't return a valid response. Check if the API provider supportes OpenAI response format.")

    return assistant_reply


def response_to_action(msg) -> str:
    """
    Converts a response from the LLM to an action.

    Args:
        msg (str): The response from the LLM.

    Returns:
        str: The action to take.
    """

    pattern = r"```json(.*?)```"
    matches = re.findall(pattern, msg, re.DOTALL)
    if not matches:
        raise Exception("Invalid response format from LLM. Expected JSON code block.")
    json_codes = matches[0].strip()

    text = json.loads(json_codes)

    codes = text["codes"]

    for section in codes:
        file = section["file"]
        code = section["code"].replace("%linefeed%", "\n")

        paths = file.split("/")

        # Join the list elements to form a path
        path = os.path.join(*paths)

        # Get the directory path and the file name
        dir_path, file_name = os.path.split(path)

        # Create directories, if they don't exist
        try:
            os.makedirs(dir_path, exist_ok=True)
        except FileNotFoundError:
            pass

        # Create the file
        with open(path, "w") as f:
            f.write(code)  # Write an empty string to the file


def mixed_decode(text: str) -> str:
    """
    Decode a mixed text containing both normal text and a byte sequence.

    Args:
        text (str): The mixed text to be decoded.

    Returns:
        str: The decoded text, where the byte sequence has been converted to its corresponding characters.

    """
    # Split the normal text and the byte sequence
    # Assuming the byte sequence is everything after the last colon and space ": "
    try:
        normal_text, byte_text = text.rsplit(": ", 1)
    except (TypeError, ValueError):
        # The text only contains normal text
        return text

    # Convert the byte sequence to actual bytes
    byte_sequence = byte_text.encode(
        "latin1"
    )  # latin1 encoding maps byte values directly to unicode code points

    # Detect the encoding of the byte sequence
    detected_encoding = chardet.detect(byte_sequence)
    encoding = detected_encoding["encoding"]

    # Decode the byte sequence
    decoded_text = byte_sequence.decode(encoding)

    # Combine the normal text with the decoded byte sequence
    final_text = normal_text + ": " + decoded_text
    return final_text

def decompile_jar(jar_path: str, output_dir: str) -> bool:
    """
    Decompiles a JAR file using the CFR tool.

    Args:
        jar_path (str): Path to the JAR file to be decompiled.
        output_dir (str): Directory where the decompiled source code will be saved.

    Returns:
        bool: True if decompilation is successful, False otherwise.
    """
    CFR_JAR_PATH = os.path.join("lib", "cfr-0.152.jar")
    
    
    # Remove the output directory if it already exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # Run CFR to decompile the JAR file
    try:
        print("Starting JAR decompilation...")
        command = [
            "java", "-jar", CFR_JAR_PATH, jar_path, "--outputdir", output_dir
        ]
        subprocess.run(command, check=True)
        print(f"Decompilation complete. Source code saved to {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Decompilation failed: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def code_to_text(directory: str) -> str:
    """
    Converts the code in a directory to text.

    Args:
        directory (str): The directory containing the code files.

    Returns:
        str: The text representation of the code.
    
    Return Structure:
        file1_path:
        ```
        1  code
        2  code
        ...
        ```
        file2_path:
        Cannot load non-text file
        ...
    """
    def is_text_file(file_path):
        txt_extensions = [
            ".txt",
            ".java",
            ".py",
            ".md",
            ".json",
            ".yaml",
            ".yml",
            ".xml",
            ".toml",
            ".ini",
            ".js",
            ".groovy",
            ".log",
            ".properties",
            ".cfg",
            ".conf",
            ".bat",
            ".sh",
            "README",
        ]
        return any(file_path.endswith(ext) for ext in txt_extensions)

    text = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            
            if is_text_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Add line numbers to content
                        numbered_lines = [f"{i+1:<3} {line}" for i, line in enumerate(content.splitlines())]
                        numbered_content = '\n'.join(numbered_lines)
                        text += f"{relative_path}:\n```\n{numbered_content}\n```\n"
                except Exception as e:
                    text += f"{relative_path}: Cannot load non-text file\n"
            else:
                text += f"{relative_path}: Cannot load non-text file\n"
    
    return text
    

def parse_edit_response(edit_response: str):
    """
    Parses a string containing code diff blocks and extracts the diff content.

    Takes an edit response string containing code diffs formatted in markdown and extracts
    the content between ```diff and ``` tags.

    Args:
        edit_response (str): A string containing one or more markdown code diff blocks

    Returns:
        list[str]: A list of strings containing the extracted diff content, with leading/trailing whitespace removed
    """
    pattern = r"```diff(.*?)```"
    matches = re.findall(pattern, edit_response, re.DOTALL)
    diffs = [m.strip() for m in matches]
    return diffs

def apply_diff_changes(diffs: list[str], decomplied_path) -> bool:
    """
    Applies the changes specified in a list of diff blocks.

    Args:
        diffs (list[str]): A list of strings containing diff blocks

    Returns:
        array(bool, string): 
            bool: True if the changes were successfully applied, False otherwise
            string: The message.
    
    Example Diff:
        diff --git a/test.txt b/test.txt
        --- a/test.txt
        +++ b/test.txt
        -strawberry
        +apple
        @@ -2,5 +2,5 @@
    """
    for diff in diffs:
        lines = diff.split("\n")

        # Ignore the first line.

        # The second and third lines contain the file paths.
        original_file = None
        modified_file = None

        for line in lines:
            #####################
            logger(f"Handling pointing line: {line}")
            if line.startswith("---"):
                logger(f"Found original file path: {line}")
                original_file = line.split("---")[-1].strip()
                original_file = original_file.replace(original_file.split("/")[0], decomplied_path, 1)
            elif line.startswith("+++"):
                logger(f"Found modified file path: {line}")
                modified_file = line.split("+++")[-1].strip()
                modified_file = modified_file.replace( modified_file.split("/")[0] , decomplied_path, 1)

        if original_file is None or modified_file is None:
            return (False, f"One of your diffs is missing the file paths. (eg. --- a/test.txt and +++ b/test.txt).\nThe error diff content: {diff}")
        
        # The remaining lines contain the diff.
        diff_lines = lines[3:]
        diff_codes = "\n".join(diff_lines)

        # Apply diff with diff.py
        with open(original_file, "r") as file:
            original_content = file.read()

        # try:
        #     result = apply_patch(original_content, diff_codes)
        # except:
        #     return (False, f"One of your diffs has a syntax error. Please check and fix your diff.\nThe error diff content: {diff}")

        result = apply_patch(original_content, diff_codes)

        with open(modified_file, "w") as file:
            file.write(result)

    return (True, "")


if __name__ == "__main__":
    print("This script is not meant to be run directly. Please run console.py instead.")
