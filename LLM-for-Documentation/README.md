# Generating project documentation with LLM

This POC shows how to leverage freeware(Llama 3.2) and open source(Granite 7b Instruct) LLMs to generate Markdown documentation for Java, .NET, and Node.js projects. We employ the Llama 3.2 3b and Granite 7b Instruct models to create detailed, structured documentation. The scripts are gernated by LLM with minor code edits and refinements.

## Generating Project Documentation Using the Llama 3.2 Model

1. Downlod the **generate_docs.py** script fie.
2. Download and serve Llama 3.2 quantized model with llama-server as shown below. This will serve the model on localhost at port 8081. 
     ```
     llama-server -m ../instructlab/models/Llama-3.2-3B-Instruct-Q8_0.gguf --port 8081
     ```
3. Execute the documentation generation script by providing the GitHub project repository URL and the Llama 3.2 service URL as arguments.
     ```
     python generate_docs.py https://github.com/bigcommerce/sample-app-nodejs.git http://localhost:8081/completion
     ```
4. The script will generate the project Markdown documentation file, DOCUMENTATION.md, in the current folder.
   
## Generating Project Documentation Using the Granite 7b Instruct Model

1. Downlod the **generate_docs_granite.py** script fie.
2. Download and serve Granite 7b Instruct quantized model with ilab as shown below. This will serve the model on localhost at port 8000. 
     ```
      ilab model serve --model-path ../models/granite-7b-instruct.Q4_K_M.gguf
     ```
3. Execute the documentation generation script by providing the GitHub project repository URL and the Granite 7b Instuct service URL as arguments.
     ```
     python generate_docs_granite.py https://github.com/bigcommerce/sample-app-nodejs.git http://localhost:8000/v1/chat/completions
     ```
4. The script will generate the project Markdown documentation file, DOCUMENTATION-granite.md, in the current folder.

### Note: I have uploaded the output documentation files from both models, DOCUMENTATION-llama.md and DOCUMENTATION-granite.md, to this project for your reference. While the default outputs from both models are impressive, I find the Granite model's output to be crisper and of higher quality. The results can be further refined by enhancing the prompts and/or fine-tuning the models. I have also uploaded output from llama 3.2 8b (Llama-3.2-8B-Instruct.Q5_K_S.gguf) moldel (DOCUMENTATION-llama8b.md) for your reference.
