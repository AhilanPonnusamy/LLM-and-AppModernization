import os
import requests
import sys
from pathlib import Path
import subprocess

def query_vllm(prompt, llm_url):
    """Send a prompt to the vLLM server and return the response."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",  # Model name for vLLM
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        print(f"Prompt sent to LLM:\n{prompt}\n")
        response = requests.post(llm_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        # Extract the response text
        return response_data["choices"][0]["message"]["content"].strip() if "choices" in response_data else "No response content received."
    except requests.RequestException as e:
        print(f"Error communicating with vLLM server: {e}")
        return "ERROR: Failed to fetch response"

def clone_repo(repo_url):
    """Clone the given Git repository into the current directory."""
    repo_name = os.path.basename(repo_url.rstrip("/").split("/")[-1]).replace(".git", "")
    try:
        subprocess.run(["git", "clone", repo_url], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to clone repository: {repo_url}")
        sys.exit(1)
    return repo_name

def generate_test_cases(repo_path, llm_url):
    """Generate test case files for code files."""
    test_folder = Path("test_generated")
    test_folder.mkdir(exist_ok=True)

    for root, _, files in os.walk(repo_path):
        for file_name in files:
            file_path = Path(root) / file_name
            if file_path.suffix != ".java":  # Restrict to Java files
                continue

            print(f"Processing file: {file_path}...")

            with open(file_path, "r") as file:
                code_content = file.read()

            # Skip empty files
            if not code_content.strip():
                print(f"Skipping empty file: {file_name}")
                continue

            # Analyze functions in the file
            prompt = f"""Analyze the following .java code and generate unit test cases for all functions/methods, including edge cases. Output well-structured test code:

{code_content}"""
            response = query_vllm(prompt, llm_url)

            if response.startswith("ERROR"):
                print(f"Error generating test cases for {file_name}. Skipping...")
                continue

            # Save the test cases to a file
            relative_path = os.path.relpath(file_path, repo_path)
            test_file_name = test_folder / (relative_path.replace("/", "_") + "_Test.java")
            test_file_name.parent.mkdir(parents=True, exist_ok=True)

            with open(test_file_name, "w") as test_file:
                test_file.write(response)

            print(f"Test cases saved in '{test_file_name}'.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_test_files.py <git_repo_url> <llm_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    llm_url = sys.argv[2]

    # Clone the repository
    repo_name = clone_repo(repo_url)

    # Generate test cases
    generate_test_cases(repo_name, llm_url)

if __name__ == "__main__":
    main()
