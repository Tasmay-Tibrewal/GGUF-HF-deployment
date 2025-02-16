import subprocess
import json
import streamlit as st
import streamlit.components.v1 as components
import os
import stat
import socket
import time

env_var = "ran_script_once"
host = "127.0.0.1"
port = 8081

prompt_format = \
'''Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

## Instruction:
Normalize entities in a given sentence, including dates (various formats), currencies (multiple symbols and notations), and scientific units (single and compound). Convert them into their full, standardized textual representations in the same language.

### Example Input:
15/03/1990 को, वैज्ञानिक ने $120 में 500mg यौगिक का एक नमूना खरीदा।

### Example Response:
पंद्रह मार्च उन्नीस सौ नब्बे को, वैज्ञानिक ने एक सौ बीस अमेरिकी डॉलर में पाँच सौ मिलीग्राम यौगिक का एक नमूना खरीदा।

Just as entities like dates, currencies, and scientific units have been normalized into simple terms, you must do the same. Do not leave any entity un-normalised.

## Input:
{}

## Response:
{}'''

def is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Set a timeout in case nothing is listening
        try:
            sock.connect((host, port))
            return True
        except (ConnectionRefusedError, socket.timeout):
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

def infer(prompt):
    print(f"Prompt:\n{prompt}\n")
    # st.write(command)
    prompt = prompt_format.format (
        prompt, # input
            "", # output - leave this blank for generation!
    )

    prompt = prompt.replace('\n','\\n')

    command = \
    '''curl --request POST \
        --url http://localhost:8081/completion \
        --header "Content-Type: application/json" \
        --data '{"prompt": "'''+prompt+'''", "n_predict": 256}\''''

    print("executing llm run command ... \n")
    # st.write("executing llm run command ... \n")

    print(f"Command:\n{command}\n")
    # st.write(f"Command: {command}")

    # Display the variable on the page
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = json.loads(result.stdout)['content']
    print(f"LLM run command Output:\n{output}\n")
    return output

def setup():
    # Get current permissions and add the execute bit for the owner
    current_permissions = os.stat("init.sh").st_mode
    os.chmod("init.sh", current_permissions | stat.S_IXUSR)
    os.chmod("init2.sh", current_permissions | stat.S_IXUSR)

    # Check if the environment variable exists
    if env_var not in os.environ:
        # Execute the init.sh script
        print(f"{env_var} does not exist")
        # st.write(f"{env_var} does not exist")
        try:
            # result = subprocess.run(["bash", "init.sh"], check=True, capture_output=True, text=True)
            # print("Script output:")
            # print(result.stdout)
            subprocess.run(["bash", "init.sh"], check=True, text=True)
            # st.write("Script output:")
            # st.write(result.stdout)
            while not is_port_in_use(host, port):
                print(f"Not listening on port: {host}:{port}")
                print("Waiting 10 seconds before retrying...")
                # st.write(f"Not listening on port: {host}:{port}")
                # st.write("Waiting 10 seconds before retrying...")
                time.sleep(10)
            print(f"Listening on port: {host}:{port}")
            # st.write(f"Listening on port: {host}:{port}")
        except subprocess.CalledProcessError as e:
            print("An error occurred:")
            print(e.stderr)
            # st.write("An error occurred:")
            # st.write(e.stderr)
        os.environ[env_var] = "1"
        print(f"{env_var} is set to 1.")
        # st.write(f"{env_var} is set to 1.")

    else:
        print(f"{env_var} exists with value: {os.environ[env_var]}")
        # st.write(f"{env_var} exists with value: {os.environ[env_var]}")
        if is_port_in_use(host, port):
            print(f"Something is listening on {host}:{port}")
            print("No need to execute anything")
            # st.write(f"Something is listening on {host}:{port}")
            # st.write("No need to execute anything")
        else:
            print(f"Nothing is listening on {host}:{port}")
            print("Executing init2.sh")
            # st.write(f"Nothing is listening on {host}:{port}")
            # st.write("Executing init2.sh")
            try:
                # result = subprocess.run(["bash", "init2.sh"], check=True, capture_output=True, text=True)
                # print("Script output:")
                # print(result.stdout)
                subprocess.run(["bash", "init2.sh"], check=True, text=True)
                # st.write("Script output:")
                # st.write(result.stdout)
            except subprocess.CalledProcessError as e:
                print("An error occurred:")
                print(e.stderr)
                # st.write("An error occurred:")
                # st.write(e.stderr)

    _ = infer("हा अहवाल 30 pages लांब आणि 10 MB आकाराचा आहे.")
    # output = "hello me tasmay!"
    # time.sleep(5)
    # st.write(f"Output:\n{output}")
    print("All setup execution is completed.")

def main():
    start_time = time.time()
    # Show a spinner while the app is setting up.
    if "setup_done" not in st.session_state:
        with st.spinner("Setting up the app, please wait. It may take around 6-7 minutes to setup."):
            setup()
        st.session_state["setup_done"] = True
    else:
        pass
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Elapsed time till complete setup: {elapsed:.2f} seconds")

    st.title("Sarvam AI - Entity Normalisation App")

    # Use a form so that pressing Enter in the text input triggers submission.
    with st.form(key="llm_form"):
        user_input = st.text_input("Enter your text:")
        submit = st.form_submit_button("Submit")

    if submit:
        # Display a loading spinner for 5 seconds to simulate processing delay.
        with st.spinner('Loading output...'):
            output_text = infer(user_input)

        st.subheader("Output:")
        # Show uneditable output text area.
        st.text_area("Model generated response", output_text, height=150, key="output_area", disabled=True)

        # Safely dump the output text as a JSON string for JS.
        output_json = json.dumps(output_text)

        # HTML/JavaScript code for the copy button.
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <script>
            function copyText() {{
                var text = {output_json};
                navigator.clipboard.writeText(text).then(function() {{
                    var btn = document.getElementById('copy_btn');
                    btn.innerText = 'Copied!';
                    setTimeout(function() {{
                        btn.innerText = 'Copy Output';
                    }}, 2000);
                }}, function(err) {{
                    console.error('Failed to copy text: ', err);
                }});
            }}
          </script>
        </head>
        <body>
          <button id="copy_btn" onclick="copyText()" style="
            padding: 0.5em 1em;
            font-size: 1em;
            margin-top: 0.5em;
            border: none;
            border-radius: 4px;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
          ">
            Copy Output
          </button>
        </body>
        </html>
        """
        # Embed the HTML. Adjust the height as needed.
        components.html(html_code, height=120)

if __name__ == "__main__":
    main()