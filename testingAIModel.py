# ollama_chat.py
import requests
import json

ollama_url = "http://localhost:11434/api/generate"

user_model_choice = input("please choose either 1 (llama3.1:8b) or 2 (gemma3:4b)")
if user_model_choice == '1':
    model = "llama3.1:8b"
else:
    model = "gemma3:4b"

agent_template = (
    "Your task is to summarise any text I give you into exactly five words. "
    "Do not ask for clarification; always respond with only the summary."
)

print("\nRainn Agent Chat (Ollama local model)")
print("Type 'exit' or 'quit' to end the conversation.\n")

# 1️⃣ Infinite chat loop
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Ending chat. Goodbye!")
        break

    # 2️⃣ Create payload (JSON)
    full_prompt = full_prompt = f"{agent_template}\n\nText: {user_input}\nSummary:"

    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": True  # allows text to appear as it’s generated
    }

    try:
        # 3️⃣ Send POST request with streaming enabled
        with requests.post(ollama_url, json=payload, stream=True) as response:
            if response.status_code != 200:
                print(f"⚠️ Error: {response.status_code} - {response.text}")
                continue

            print("AI:", end=" ", flush=True)
            for line in response.iter_lines():
                if line:
                    # Ollama returns JSON lines — decode and print them
                    data = json.loads(line.decode("utf-8"))
                    content = data.get("response", "")
                    print(content, end="", flush=True)
            print("\n")  # newline after model finishes

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Ollama. Make sure 'ollama serve' is running.")
    except Exception as e:
        print("⚠️ Error:", e)
