# Generating Unit Tests with LLM

This POC shows how to leverage open source(Granite 7b Instruct) LLMs to generate code summary for SpringBoot(Java) projects. We employ Granite 7b Instruct model to create unit tests for all the files in the project under test_generated folder.The generated test files can be used by developers as a gudeline to build unit tests for their code. The script is gernated by LLM with minor code edits and refinements.

   
## Generating Unit Tests Using the Granite 7b Instruct Model

1. Downlod the **generate_tests.py** script fie.
2. Download and serve Granite 7b Instruct quantized model with ilab as shown below. This will serve the model on localhost at port 8000. 
     ```
      ilab model serve --model-path ../models/granite-7b-instruct.Q4_K_M.gguf
     ```
3. Execute the test cases generation script by providing the GitHub project repository URL and the Granite 7b Instuct service URL as arguments.
     ```
     python generate_tests.py https://github.com/nevenc/spring-music-k8s.git http://localhost:8000/v1/chat/completions
     ```
4. The script will generate unit tests under the test_generated folder.

