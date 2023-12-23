# LLM-and-AppModerization - Fine Tuning

## Detailed explanation of this POC is provided in this [blog](https://medium.com/@ahilanp/part-ii-poc-beyond-the-buzz-highlighting-the-impact-of-ai-in-modernizing-application-ff0c1e8efb87) ##

This exercise is the extension on the XBC Bank POC that we discussed earlier. In this exercise we will achieve the following

1. Use training data that is created for the XBC Bank usecase
2. Fine tune the base **Llama-2-70b-chat-hf** model with the training data in Google Colab 
3. Upload the fine tuned model to your Hugging Face repository
   
**System Specifications: (Same as the previous exercise)**

- Device: MacBook Pro
- Processor: 2.6 GHz 6-Core Intel Core i7
- RAM: 32 GB 2667 MHz DDR4

Follow the outlined steps to seamlessly set up Llama2 on your local environment. You may be able to follow the instruction for both Mac or Windows machine.

## STEP 1: Fine tuning the Llama2 chat model in Google Colab with XBC bank training data

1. I used Google Colab (https://colab.research.google.com/?utm_source=scs-index) for this task. While the free version might work sometimes, it can be slow, or you might get timed out because of limited resources. I strongly suggest either getting compute units under the **Pay As You Go** model or subscribing to Colab Pro. For this task, I bought 100 Pay As You Go compute units. Even after all the testing, I only used 18 compute units, which cost around $2 USD.

2. Open **Fine-Tuning/XBC_Fine_tune_Llama_2_in_Google_Colab.ipynb**. Right click on **Open in Colab** button on the top left corner. and open it in a new tab. It will open the the script in Google Colab. 

3. Create a folder called **data** by selecting the "New Folder" option on right click in folder tab as shown below.
   ![Colab UI](../images/colab.png)

4. Download **train.csv** file from this folder(Fine-Tuning Folder) and upload it to **Colab->data** folder that you just created by selecting **Upload** option on right click as shown below.
   ![Colab UI](../images/colab-trainingfile.png)


5. You are all set to execute the Fine tuning script now. Execute one cell at a time by clicking on the Run button as shown below
   ![Colab UI](../images/Colab-runscript.png)

 >[!WARNING]
 >DO NOT RUN ALL THE CELLS AT THE SAME TIME, DOING SO MIGHT THROW OUT OF MEMORY ERROR LATER IN THE SCRIPT.

6. After executing Cell 7 to clear the VRAM, please restart the runtime by selecting **Runtime->Restart Session** option. This will help to ensure the memory is flushed and is ready for building the combined model in the next two steps.
   ![Colab UI](../images/colab-clearRAM.png)

7. **Re-execute the first three cells again to setup the environment**. 
 >[!NOTE]
 >Execute only the first 3 cells. Executing beyond that is not required.
   
8. Execute Cell 8 to reload and merge the model.
   ![Colab UI](../images/colab-buildmodel.png) 

9. **[Optional]** Run Cell 9 to push the Fine tuned model to your Hugging Face Repository. You will need a write access token fort this. Create a write Access Token under profile if you do not have one.

## STEP 2: Building GGUF file for local execution 

In this section, we will build GGUF format for the fine tuned Llama2 chat model created in STEP 1.

1.  In a new terminal, Install huggingface_hub library
   
```
     pip install huggingface_hub
```

2. Fetch the HuggingFace model we stored in your Hugging Face account in STEP1

```
   from huggingface_hub snapshot_download
   
   model_id="AhilanPonnusamy/llama-2-7b-xbcfinetuned"
   snapshot_download(repo_id=model_id, local_dir="XBCllama-hf",
                  local_dir_use_symlinks=False, revision="main")
```

 >[!NOTE]
 >If desired, replace the **model_id** with your Hugging Face repository details. If you use your repository you will not have the **tokenizer.model** file which is required to build the GGUF format. You can either download it from **AhilanPonnusamy/llama-2-7b-xbcfinetuned** or from the 
 >base model repository **NousResearch/Llama-2-7b-chat-hf**. Make sure tokenizer.model file is available in your Hugging Face repository before moving to the next step.

3. Install llama.cpp if it is not done already

```
  $ git clone https://github.com/ggerganov/llama.cpp.git

  $ pip install -r llama.cpp/requirements.txt
```

4. Execute the converion script to build the GGUF model

```
  $ python llama.cpp/convert.py XBCllama-hf \
    --outfile llama-2-7b-xbcfinetuned-q8_0-gguf \
    --outtype q8_0
```

5. Test the model from llama.cpp folder

```
 ./main -m ../llama-2-7b-xbcfinetuned-q8_0-gguf --color -ins -n -1
```
![Colab UI](../images/finetuned-chat.jpg) 

***Have fun!!!!!***

