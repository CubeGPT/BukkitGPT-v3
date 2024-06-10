from openai import OpenAI
import chardet
import sys
import json
import locale
import os

from log_writer import logger
import config

def initialize():
    """
    Initializes the software.

    This function logs the software launch, including the version number and platform.

    Args:
        None

    Returns:
        None
    """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    logger(f"Launch. Software version {config.VERSION_NUMBER}, platform {sys.platform}")

def askgpt(system_prompt: str, user_prompt: str, model_name: str, disable_json_mode: bool = False, image_url: str = None):
    """
    Interacts with ChatGPT using the specified prompts.

    Args:
        system_prompt (str): The system prompt.
        user_prompt (str): The user prompt.
        model_name (str): The model name to use.
        disable_json_mode (bool): Whether to disable JSON mode.

    Returns:
        str: The response from ChatGPT.
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
            {"role": "user", "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]


    logger(f"askgpt: system {system_prompt}")
    logger(f"askgpt: user {user_prompt}")

    # Create a chat completion
    if disable_json_mode:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
    else:
        response = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=messages
        )

    logger(f"askgpt: response {response}")

    # Extract the assistant's reply
    assistant_reply = response.choices[0].message.content
    logger(f"askgpt: extracted reply {assistant_reply}")
    return assistant_reply

def response_to_action(msg):
    """
    Converts a response from ChatGPT to an action.

    Args:
        msg (str): The response from ChatGPT.

    Returns:
        str: The action to take.
    """
    text = json.loads(msg)

    codes = text["codes"]

    for section in codes:
        file = section["file"]
        code = section["code"]

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
        with open(path, 'w') as f:
            f.write(code)  # Write an empty string to the file

def mixed_decode(text: str):
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
    byte_sequence = byte_text.encode('latin1')  # latin1 encoding maps byte values directly to unicode code points

    # Detect the encoding of the byte sequence
    detected_encoding = chardet.detect(byte_sequence)
    encoding = detected_encoding['encoding']

    # Decode the byte sequence
    decoded_text = byte_sequence.decode(encoding)

    # Combine the normal text with the decoded byte sequence
    final_text = normal_text + ": " + decoded_text
    return final_text

if __name__ == "__main__":
    print("This script is not meant to be run directly. Please run console.py instead.")