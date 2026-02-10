
import requests\
import logging\
from tkinter import messagebox, filedialog\
\
API_KEY = '' # Insert API Key here
JASMIN_GUIDE_LINK = "https://jasmin-lang.github.io/jasmin/reference-manual.pdf"  # Substitute with actual user guide link\
\
def load_prompt_from_file():\
    """Load prompt from a local text file selected by the user"""\
    file_path = filedialog.askopenfilename(\
        title="Select Prompt File",\
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]\
    )\
    \
    if not file_path:\
        return None\
    \
    try:\
        with open(file_path, 'r', encoding='utf-8') as file:\
            prompt_content = file.read().strip()\
            return prompt_content\
    except Exception as e:\
        messagebox.showerror("File Error", f"Failed to read prompt file: \{e\}")\
        return None\
\
def fetch_bytecode_slice(repo_url, prompt_content):\
    """Fetch bytecode slice using the provided prompt content"""\
    if not prompt_content:\
        messagebox.showwarning("Prompt Error", "No prompt content loaded.")\
        return None\
    \
    # Replace placeholder in prompt if it exists\
    formatted_prompt = prompt_content.replace("\{REPO_URL\}", repo_url).replace("\{JASMIN_GUIDE_LINK\}", JASMIN_GUIDE_LINK)\
\
    \
    payload = \{\
        "model": "sonar",\
        "messages": [\
            \{"role": "system", "content": "You are a skilled software reverse engineering assistant."\},\
            \{"role": "user", "content": formatted_prompt\}\
        ],\
        "max_tokens": 3000,\
        "temperature": 0.0\
    \}\
    headers = \{\
        'Authorization': f'Bearer \{API_KEY\}',\
        'Content-Type': 'application/json'\
    \}\
    url = "https://api.perplexity.ai/chat/completions"\
    logging.info("sending request to perplexity")\
    response = requests.post(url, headers=headers, json=payload)\
    logging.info("sent prompt")\
    return response.json()\
\
def handle_submit():\
    repo_url = entry.get().strip()\
    if not repo_url:\
        messagebox.showwarning("Input Error", "Please enter a GitHub repository link.")\
        return\
    \
    # Load prompt from file\
    prompt_content = load_prompt_from_file()\
    if not prompt_content:\
        return\
    \
    try:\
        bytecode_response = fetch_bytecode_slice(repo_url, prompt_content)\
        # Extract just the text answer (if result format matches documented API)\
        bytecode_text = ""\
        try:\
            bytecode_text = bytecode_response['choices'][0]['message']['content']\
        except Exception as e:\
            bytecode_text = f"Error: Could not extract bytecode from response.   \\n\\nFull API Response:\\n\{bytecode_response\}"\
\
        result_text.delete("1.0", tk.END)\
        result_text.insert(tk.END, bytecode_text)\
\
        # Optionally store for save/download\
        global last_bytecode_text\
        last_bytecode_text = bytecode_text\
    except Exception as e:\
        messagebox.showerror("Error", f"Failed to fetch bytecode: \{e\}")\
\
def load_prompt_file():\
    """Button handler to load and preview prompt file content"""\
    prompt_content = load_prompt_from_file()\
    if prompt_content:\
        # Show a preview of the loaded prompt in a new window\
        preview_window = tk.Toplevel(root)\
        preview_window.title("Prompt File Preview")\
        preview_window.geometry("600x400")\
        \
        preview_text = tk.Text(preview_window, wrap='word', height=20, width=70)\
        preview_text.pack(padx=10, pady=10, fill='both', expand=True)\
        preview_text.insert(tk.END, prompt_content)\
        preview_text.config(state='disabled')  # Make it read-only\
        \
        close_button = tk.Button(preview_window, text="Close", command=preview_window.destroy)\
        close_button.pack(pady=5)\
\
def save_bytecode_to_file():\
    if not last_bytecode_text.strip():\
        messagebox.showwarning("No Bytecode", "There's no bytecode to save.")\
        return\
    file_path = filedialog.asksaveasfilename(\
        title="Save Bytecode As",\
        defaultextension=".txt",\
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]\
    )\
    if not file_path:\
        return\
    try:\
        with open(file_path, 'w', encoding='utf-8') as f:\
            f.write(last_bytecode_text)\
        messagebox.showinfo("Saved", f"Bytecode saved to \{file_path\}")\
    except Exception as e:\
        messagebox.showerror("Save Error", f"Failed to save file: \{e\}")\
\
\
# Create main window\
root = tk.Tk()\
root.title("GitHub Repo to Jasmin Bytecode Slice")\
\
# Repository input\
label = tk.Label(root, text="Enter GitHub Repository Link:")\
label.pack(padx=10, pady=10)\
\
entry = tk.Entry(root, width=55)\
entry.pack(padx=10, pady=5)\
\
# Buttons frame\
button_frame = tk.Frame(root)\
button_frame.pack(padx=10, pady=8)\
\
load_prompt_button = tk.Button(button_frame, text="Load Prompt File", command=load_prompt_file)\
load_prompt_button.pack(side=tk.LEFT, padx=(0, 5))\
\
submit_button = tk.Button(button_frame, text="Submit", command=handle_submit)\
submit_button.pack(side=tk.LEFT, padx=(5, 0))\
\
download_button = tk.Button(button_frame, text="Download Bytecode", command=save_bytecode_to_file)\
download_button.pack(side=tk.LEFT, padx=(5, 0))\
\
\
# Results display\
result_text = tk.Text(root, wrap='word', height=20, width=75)\
result_text.pack(padx=10, pady=10)\
\
# Instructions label\
instructions = tk.Label(root, text="1. Click 'Load Prompt File' to select your prompt file\\n2. Enter repository URL\\n3. Click 'Submit'", \
                       justify=tk.LEFT, fg="gray")\
instructions.pack(padx=10, pady=(0, 10))\
\
root.mainloop()\
\
}
