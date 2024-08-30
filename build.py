from subprocess import Popen, PIPE, STDOUT
from log_writer import logger


def build_plugin(artifact_name):
    project_path = f"codes/{artifact_name}"
    build_command = [
        "cd",
        project_path,
        "&&",
        "mvn",
        "-V",
        "-B",
        "clean",
        "package",
        "--file",
        "pom.xml",
    ]

    process = Popen(build_command, stdout=PIPE, stderr=STDOUT, shell=True)

    def log_subprocess_output(pipe):
        output = ""
        for line in iter(pipe.readline, b""):
            str_line = str(line)
            output += str_line
            logger(f"building -> {str_line}")
        return output

    with process.stdout:
        output = log_subprocess_output(process.stdout)

    process.wait()

    return output


if __name__ == "__main__":
    result = build_plugin("ExamplePlugin2")
    print(result)
    print(type(result))
