import os
import requests
import sys
from pathlib import Path
import json
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


def generate_code_comments(repo_path, llm_url):
    """Generate comments for code files and save in a JSON format."""
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
            prompt = f"Analyze the following {extension} code and generate comments for all functions/methods. Include a summary comment at the top of the file.\n\n{code_content}"
            response = query_vllm(prompt, llm_url)

            if response.startswith("ERROR"):
                print(f"Error generating comments for {file_name}. Skipping...")
                continue

            # Save the comments in JSON format
            relative_path = os.path.relpath(file_path, repo_path)
            comment_data[relative_path] = response

    # Save the JSON to disk
    json_path = Path("code_summary.json")
    with open(json_path, "w") as json_file:
        json.dump(comment_data, json_file, indent=4)
    
    print(f"Code comments saved in '{json_path.resolve()}'.")


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_docs.py <git_repo_url> <llm_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    llm_url = sys.argv[2]

    # Clone the repository
    repo_name = clone_repo(repo_url)

    # Generate code comments
    generate_code_comments(repo_name, llm_url)


if __name__ == "__main__":
    main() 