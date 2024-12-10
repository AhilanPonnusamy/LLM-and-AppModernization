import os
import requests
import sys
from pathlib import Path
import json
import subprocess


def query_llama_server(prompt, server_url="http://localhost:8080/completion", max_tokens=200):
    """Sends a prompt to the LLaMA server and returns the response."""
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.3,
        "top_p": 0.9,
    }

    try:
        response = requests.post(f"{server_url}", json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("content", "No response text received")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with LLaMA server: {e}"


def clone_repo(repo_url):
    """Clone the given Git repository into the current directory."""
    repo_name = os.path.basename(repo_url.rstrip("/").split("/")[-1]).replace(".git", "")
    try:
        subprocess.run(["git", "clone", repo_url], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to clone repository: {repo_url}")
        sys.exit(1)
    return repo_name


def generate_code_comments(repo_path, llama_server_url):
    """Generate comments for code files and save them in a JSON format."""
    comment_data = {}
    file_extensions = {
        ".java": "//",
        ".js": "//",
        ".ts": "//",
        ".cs": "//"
    }

    for root, _, files in os.walk(repo_path):
        for file_name in files:
            file_path = Path(root) / file_name
            extension = file_path.suffix
            if extension not in file_extensions:
                continue

            print(f"Processing file: {file_path}...")

            with open(file_path, "r") as file:
                code_content = file.read()

            # Skip empty files
            if not code_content.strip():
                print(f"Skipping empty file: {file_name}")
                continue

            # Analyze functions in the file
            prompt = (
                f"Analyze the following {extension} code and generate a detailed comment that includes "
                f"a summary of the file and describes the main purpose and functionality.\n\n{code_content}"
            )
            response = query_llama_server(prompt, server_url=llama_server_url)

            if "Error" in response:
                print(f"Error generating comments for {file_name}: {response}. Skipping...")
                continue

            # Parse the response and save the comments
            relative_path = os.path.relpath(file_path, repo_path)
            comment_data[relative_path] = response

    # Save the JSON to disk
    json_path = Path("code_summary.json")
    with open(json_path, "w") as json_file:
        json.dump(comment_data, json_file, indent=4)
    
    print(f"Code comments saved in '{json_path.resolve()}'.")


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_docs.py <git_repo_url> <llama_server_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    llama_server_url = sys.argv[2]

    # Clone the repository
    repo_name = clone_repo(repo_url)

    # Generate code comments
    generate_code_comments(repo_name, llama_server_url)


if __name__ == "__main__":
    main()
