# GGUF-HF-deployment
Github version of my hugging face space's repo. Deployed the gguf version of my finetuned llama model, using streamlit on HF spaces for free, using llama.cpp. 

Deployed the model: `Tasmay-Tib/sarvam-entity-normalisation-llama-3.1-8b-gguf`, which is the gguf version of the model: `Tasmay-Tib/sarvam-entity-normalisation-llama-3.1-8b` on Hugging Face spaces.

Model application lies in `entity normalisation` for indic languages. Model is a finetune of the `unsloth/meta-llama-3.1-8b-bnb-4bit` model, which is itself is a `4-bit` bnb quantisation of the `meta-llama/Llama-3.1-8B` model.

HF Space Link: `https://huggingface.co/spaces/Tasmay-Tib/sarvam-ai-entity-normalisation`

This runs for completely free, using llama.cpp.

Check the folder `sarvam-ai-entity-normalisation-non-git` for code, the folder `sarvam-ai-entity-normalisation` is the actual HF spaces repo and may not be viewable in GitHub. Both the directories have the same content but one is with `git` as a submodule and the other is a simple dir for viewing purposes on GitHub.

I have not-used `llama.cpp's` python binding `llama-cpp-python` since it is not optimal. I have served the model using `llama-cpp's: llama-server`, which is optimal and more efficient.

Deployed the app using streamlit, and it is a bit tough for HF free user's to control the build and installations using python. Thus this repo.

This is the `colab` notebook: [Colab](https://colab.research.google.com/drive/1riG227E1l1AXKO93BMWg3daheHKrD0ZP?usp=sharing) with different model inference methods for the `gguf` model using llama.cpp and also demonstrates the basic code of this repo, in the section: `Run using '.sh' scripts, useful for HF spaces deployment`, for easier understanding.

Take inspiration from the code to understand how to build `llama.cpp` by executing commands in `init.sh` such that the server does not collapse on command execution and then send requests (in `utf-8` format).
Note: Python `requests` library is not used for sending requests since it was not able to handle multilingual (`utf-8`) based characters properly. Thus `subprocess` execution of `curl` is used.

Also built port and host checker to check which port is free for serving. And also added in an environment variable for checking if the setup is done on a re-run, to avoid the additional setup time for each user.
Major downside of free: No storage, thus despite of the environment variable the session info is lost and the space is stopped each time, forcing for a complete re-run. An alternate is to purchase the `$0.01- 20GB` sotrage per hour, it is pretty cheap and we will not need more than `6-7 GB` storage, this will prevent the large load times of the space. LLM response time, after initial caching is about `20 seconds` for 2 vCPUs, since the output is quite small for the usecase. This can further be reduced by an estimated `~4x` using the paid cpu tier with 8 vCPUs in HF. For utilising this, change the server parameter during command run in `init.sh` from "`-t 2`" to "`-t 8`", as specified in the llama.cpp docs, for optimal performance the thread count should ideally be equal to number of cpu cores. But twenty seconds seems fine for testing purposes. Since the model itself is not trained on a lot of tokens, anything above `150-200 tokens` is too much for it, and it will probably end the answer itself. Thus the output is also limited to `256 tokens`.
