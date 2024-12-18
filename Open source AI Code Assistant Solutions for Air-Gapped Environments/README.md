# Open source AI Code Assistant for Air Gapped Deployment

## Detailed explanation of this POC is provided in this [blog](https://medium.com/@ahilanp/part-iii-fine-tuning-beyond-the-buzz-highlighting-the-impact-of-ai-in-modernizing-application-74fb748d894b) ##

This POC shows how to leverage Granite code models for building an Open source AI code assistant for secured and Air gapped environemts. It uses VS Code as the IDE and continue.dev extension as the AI Code assistant and IBM Granite code models for chat and auto completion. 

## STEP 1: Install continue.dev VS Code Extension

1. Install continue.dev extension in VS Code 
>![VS_Code_Extension](../images/Extenion.png)  
   

2. Once installed, you will see the continue.dev extension shown in the left side toolbar.
>![VS_Code_Extension_Installed](../images/Extension_Installed.png) 

## STEP 2: Download and Serve Granite code models for Chat and Code auto completion

3. For this POC we will be using two Granite code models
   1. granite-8b-code-instruct-128k.Q5_K_M.gguf model served by InstructLab for Chat.
   2. granite-code:3b model served by ollama for code completion.

 >[!NOTE]
 >You can also use the same model for both chat and code completion if you like. If you decide to use the same model for both chat and code completion, use ollama for serving the model as vLLM serving option seem to have some issues with code completion.

4. Download and serve the models in two different terminals as shown below
```
  $ ilab model serve --model-path models/granite-8b-code-instruct-128k.Q5_K_M.gguf

  $ ollama run granite-code:3b
```

## STEP 3: Configure Chat and Code auto completion models in continue extension.  

5. Select the Continue extension and click the Configure/Settings button located in the top-right corner of the Continue chat window. It will open the config.json file. 
>![VS_Code_Extension_Configuration](../images/configure-continue.png) 

6. Add the following chat model configuration under the models section. This will enable the extension to automatically detect the Granite 8B code model served by InstructLab.

```
    {
      "model": "AUTODETECT",
      "title": "Autodetect",
      "apiKey": "Empty",
      "provider": "openai",
      "apiBase": "http://localhost:8000/v1"
    }
```
 >[!NOTE]
 >You can also use the 'Add Chat Model' option to add the model, as shown below. However, you'll still need to manually add the 'apiBase' property if you choose this approach.

>![Configure_model](../images/add-chat-model-window.png)


## STEP 3: Integrate with XBC Streamlit app

1. Move the fine tuned model **llama-2-7b-xbcfinetuned-q8_0-gguf** to LLM-UI/models folder and rename it to **llama-2-7b-xbcfinetuned-q8_0-gguf.bin**.

2. Get the **app-ft.py** file from the github repository. This file uses the fine tuned model and does not include the post processing hack to adress base model issues as explained in the previous lab.

3. Start the LLM app

```
     streamlit run app-ty.py
```

4. Try various prompts from the main folder README file. You will see the responses are much more aligned with the context with less hallucination and warning messages.
>![App UI](../images/Finetuned-output.png)  
   
***Have fun!!!!!***


