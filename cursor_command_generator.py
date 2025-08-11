import subprocess
import os


ITERATION_FILE = ".agentic_loop_iteration"
MAX_ITERATIONS = 100  # Increased max iterations as requested


def get_iteration():
    if os.path.exists(ITERATION_FILE):
        with open(ITERATION_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0


def set_iteration(count):
    with open(ITERATION_FILE, "w") as f:
        f.write(str(count))


def find_and_handle_user_input_request():
    # Only look for Python files in the src directory
    src_dir = "src"
    if not os.path.exists(src_dir) or not os.path.isdir(src_dir):
        return False

    python_files = [
        os.path.join(src_dir, f) for f in os.listdir(src_dir)
        if f.endswith('.py')
    ]

    for py_file in python_files:
        with open(py_file, "r") as f:
            for line_num, line in enumerate(f, 1):
                if line.strip().startswith("# AGENTIC_INPUT_REQUIRED:"):
                    try:
                        question = line.split("# AGENTIC_INPUT_REQUIRED:",
                                              1)[1].strip()
                        if not question:
                            continue

                        print("\n--- USER INPUT REQUIRED ---")
                        print(f"File: {py_file}, Line: {line_num}")
                        print(f"Question: {question}")
                        user_answer = input("Please provide your input "
                                            "(then press Enter): ")
                        print("--- Sending input "
                              f"\"{user_answer}\" to Cursor... ---\n")

                        # Construct prompt for Cursor to use the input and
                        # re-run
                        prompt = (
                            f"Input needed in {py_file}:{line_num} "
                            f"for \"{question}\". "
                            f"Answer: \"{user_answer}\". "
                            "Integrate; then re-run "
                            f"`.venv/bin/python cursor_command_generator.py`."
                        )
                        send_to_cursor(prompt)
                        return True  # Indicates that user input was handled
                    except Exception as e:
                        print("Warning: Could not parse "
                              f"AGENTIC_INPUT_REQUIRED on line {line_num} "
                              f"of {py_file}: {e}")
    return False  # No user input required found


def run_checks():
    python_files = [f for f in os.listdir('.') if f.endswith('.py')]
    if not python_files:
        return "No Python files found to check.", True

    all_issues = []

    # Run Flake8
    flake8_cmd = [".venv/bin/flake8"] + python_files
    flake8_result = subprocess.run(flake8_cmd, capture_output=True, text=True)
    if flake8_result.stdout:
        all_issues.append(f"""--- Flake8 Issues ---
{flake8_result.stdout}""")

    # Run MyPy
    mypy_cmd = [".venv/bin/mypy"] + python_files
    mypy_result = subprocess.run(mypy_cmd, capture_output=True, text=True)
    if (mypy_result.stdout and
            "Success: no issues found" not in mypy_result.stdout):
        all_issues.append(f"""--- MyPy Issues ---
{mypy_result.stdout}""")

    if all_issues:
        return "\n\n".join(all_issues), False
    else:
        return "All code quality checks passed!", True


def send_to_cursor(command_string):
    print(command_string)


if __name__ == "__main__":
    current_iteration = get_iteration()

    # First, check for any blocking user input requests
    if find_and_handle_user_input_request():
        # If a request was handled, the script sent a prompt to Cursor
        # and exited.
        # Cursor will process the prompt and re-run the script as
        # instructed.
        pass
    elif current_iteration >= MAX_ITERATIONS:
        send_to_cursor("Maximum iterations reached. Automated "
                       "checks stopped. Please review the code "
                       "manually.")
        set_iteration(0)  # Reset for next session
    else:
        set_iteration(current_iteration + 1)
        issues, passed = run_checks()

        if passed:
            prompt = ("All code quality checks passed! You can now "
                      "proceed with other tasks or consider this "
                      "feature complete.")
            set_iteration(0)  # Reset iteration count if successful
        else:
            prompt = (
                f"I have identified the following code quality issues "
                f"in the Python files: {issues} "
                f"Please fix these issues. After you believe you "
                f"have fixed them, run this command in the "
                f"terminal: `.venv/bin/python "
                f"cursor_command_generator.py` "
                f"This is iteration {current_iteration + 1} of "
                f"{MAX_ITERATIONS}."
            )
        send_to_cursor(prompt)
