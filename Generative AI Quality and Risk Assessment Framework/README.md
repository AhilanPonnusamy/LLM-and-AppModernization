# Generative AI Quality and Risk Assessment Framework

## Detailed explanation of this POC is provided in this [blog](https://medium.com/beyond-the-buzz-highlighting-the-impact-of-ai-in/part-v-last-mile-defense-for-genai-powered-business-solutions-75a4d0e42f09) ##

## Overview

This repository contains code for a Generative AI Quality and Risk Assessment Framework. It integrates sentiment analysis, emotion detection, toxicity detection, and similarity scoring using pre-trained language models to evaluate the quality and risks associated with generated text.

## Setup

### Prerequisites

- Python 3.8+ installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AhilanPonnusamy/LLM-and-AppModernization.git
   cd LLM-and-AppModernization/Generative AI Quality and Risk Assessment Framework

2. Install virtualenv
   ```bash
   pip install virtualenv
   virtualenv myenv

3. Activate the virtual environment (use deactivate command to deactivate the virutalenv once done)
   ```bash
   source myenv/bin/activate 

4. Install all dependencies from requirements.txt file
   ```bash
   pip3 install -r requirements.txt

5. Start the Analysis service
   ```bash
   python3 QualityAnalyzer.py

6. Open a new terminal window and from the Generative AI Quality and Risk Assessment Framework folder and run the sample client application.
   ```bash
   python3 invokeAPI.py

7. Quality Analysis summary will be displayed in the screen in JSon format

***Have fun!!!!!*** 
