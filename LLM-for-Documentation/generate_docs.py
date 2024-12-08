import os
import subprocess
import tempfile
import sys
import requests
from pathlib import Path

def query_llama_server(prompt, server_url="http://localhost:8081/completion", max_tokens=5000):
    """Sends a prompt to the LLaMA server and returns the response."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.3,
        "top_p": 0.9,
    }
    try:
        response = requests.post(server_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("content", "No response content received.")
    except requests.RequestException as e:
        print(f"Error communicating with LLaMA server: {e}")
        return "ERROR: Failed to fetch response"

def clone_repo(repo_url):
    """Clone the given Git repository into a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    try:
        subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to clone repository: {repo_url}")
        sys.exit(1)
    return temp_dir

def generate_documentation(repo_path, repo_name, llama_server_url):
    """Generate Markdown documentation for all code files in a repository."""
    documentation_path = Path("DOCUMENTATION.md")
    documentation = f"# Documentation for Project: {repo_name}\n\n"
    documentation += "This document provides a description of all the source files in the repository.\n\n"

    # Supported file extensions
    file_extensions = ["*.java", "*.js", "*.ts", "*.cs"]

    code_files = []
    for ext in file_extensions:
        code_files.extend(Path(repo_path).rglob(ext))

    if not code_files:
        print("No supported code files found in the repository.")
        sys.exit(1)

    for file_path in code_files:
        filename = file_path.name
        print(f"Processing file: {filename}...")  # Real-time feedback
        with open(file_path, "r") as file:
            code_content = file.read()

        if not code_content.strip():
            print(f"Skipping empty file: {filename}")
            continue

        # Adjust the prompt based on file type
        if filename.endswith(".java"):
            language = "Java"
        elif filename.endswith(".js") or filename.endswith(".ts"):
            language = "JavaScript/TypeScript"
        elif filename.endswith(".cs"):
            language = "C# (.NET)"
        else:
            continue

        prompt = (
            f"Explain the following {language} code in Markdown format. "
            f"Provide details about its purpose, key functions, and usage.\n\n{code_content}"
        )
        explanation = query_llama_server(prompt, server_url=llama_server_url)

        documentation += f"## {filename}\n\n"
        documentation += explanation if "ERROR" not in explanation else "Documentation could not be generated for this file.\n"
        documentation += "\n---\n\n"

    documentation_path.write_text(documentation)
    print(f"\nDocumentation generated successfully in '{documentation_path.resolve()}'.\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_docs.py <git_repo_url> <llama_server_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    llama_server_url = sys.argv[2]

    # Clone the repository
    repo_path = clone_repo(repo_url)

    # Extract repository name from URL
    repo_name = os.path.basename(repo_url.rstrip("/").split("/")[-1]).replace(".git", "")

    # Generate documentation
    generate_documentation(repo_path, repo_name, llama_server_url)

if __name__ == "__main__":
    main()
