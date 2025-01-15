"""Script to compile Typst source files."""
import logging
import subprocess
import sys


def compile(in_file: str, out_file: str, options: list[str]) -> bool:
    """Compiles a Typst file with the specified global options.

    Returns True if the typst command exited with status 0, False otherwise.
    """
    command = ["typst"] + ["compile", in_file] + options + [out_file]
    logging.debug("Running: " + " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)
    try:
        result.check_returncode()
    except subprocess.CalledProcessError:
        logging.error(f"Compiling {in_file} failed with stderr: \n {result.stderr}")
        return False

    return True


def main():

    logging.basicConfig(level=logging.INFO)

    # Parse the positional arguments, expected in the following form
    #   1. The Typst files to compile in a line separated string
    #   2. The global Typst CLI options, in a line separated string. It means each
    #      whitespace separated field should be on its own line.
    logging.info(f"argv-all {sys.argv.join("~")}")
    source_files = sys.argv[1].splitlines()
    logging.info(f"argv1 {source_files}")
    output_files = sys.argv[2].splitlines()
    logging.info(f"argv2 {output_files}")
    options = sys.argv[3].splitlines()

    version = subprocess.run(
        ["typst", "--version"], capture_output=True, text=True
    ).stdout
    logging.info(f"Using version {version}")

    success: dict[str, bool] = {}

    for (in_file, out_file) in zip(source_files, output_files):
        in_file = in_file.strip()
        out_file = out_file.strip()
        if in_file == "":
            continue
        logging.info(f"compiling {in_file} as {out_file}")
        success[in_file] = compile(in_file, out_file, options)

    # Log status of each input files.
    for in_file, status in success.items():
        logging.info(f"{in_file}: {'✔' if status else '❌'}")

    if not all(success.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
