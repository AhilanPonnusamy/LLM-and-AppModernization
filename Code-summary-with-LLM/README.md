# Generating Code Summary with LLM

This POC shows how to leverage freeware(Llama 3.2) and open source(Granite 7b Instruct) LLMs to generate code summary for Java, .NET, and Node.js projects. We employ the Llama 3.2 8b and Granite 7b Instruct models to create code summary for all the files in the project in a JSON file. The scripts are gernated by LLMs with minor code edits and refinements.

## Generating Code Summary Using the Llama 3.2 Model

1. Downlod the **generate_code_summary_llama.py** script fie.
2. Download and serve Llama 3.2 quantized model with llama-server as shown below. This will serve the model on localhost at port 8081. 
     ```
     llama-server -m ../instructlab/models/Llama-3.2-8B-Instruct.Q5_K_S.gguf --port 8081
     ```
3. Execute the documentation generation script by providing the GitHub project repository URL and the Llama 3.2 service URL as arguments.
     ```
     python generate_code_summary_llama.py https://github.com/bigcommerce/sample-app-nodejs.git http://localhost:8081/completion
     ```
4. The script will generate the code summary JSON file, code_summary.json, in the current folder.
   
## Generating Code Summmary Using the Granite 7b Instruct Model

1. Downlod the **generate_code_summary.py** script fie.
2. Download and serve Granite 7b Instruct quantized model with ilab as shown below. This will serve the model on localhost at port 8000. 
     ```
      ilab model serve --model-path ../models/granite-7b-instruct.Q4_K_M.gguf
     ```
3. Execute the documentation generation script by providing the GitHub project repository URL and the Granite 7b Instuct service URL as arguments.
     ```
     python generate_code_summary.py https://github.com/bigcommerce/sample-app-nodejs.git http://localhost:8000/v1/chat/completions
     ```
4. The script will generate the code summary JSON file, code_summary.json, in the current folder.

## Note:
I have uploaded the output documentation files from both models for quarkus and node projects, code_summary_quarkus_llama8b.json, code_summary_node_llama8b.json and code_summary_quarkus_granite.json, code_summary_node_granite.json to this folder for your reference. For quarkus I used the super heros reference project available at https://github.com/quarkusio/quarkus-super-heroes.git

