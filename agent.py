import boto3
import os
from dotenv import load_dotenv
load_dotenv()

bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

output_dir = "qsr_website"
os.makedirs(output_dir, exist_ok=True)

# Call the agent
response = bedrock_agent_runtime.invoke_agent(
    agentId="KXHANQBS8O",
    agentAliasId="CA1VFT0LQ5",
    sessionId="your-session-id",
    inputText=(
        "Create a static website for a Coffe Shop named room3-Coffee. Using HTML and CSS."
    ),
)

print("\n=== Streaming Response ===\n")
for event in response["completion"]:
    if "chunk" in event:
        print(event["chunk"]["bytes"].decode("utf-8"), end="")  # optional description
    elif "files" in event:
        for file in event["files"]["files"]:
            filename = file["name"]
            file_bytes = file["bytes"]
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(file_bytes)
            print(f"\n✅ Saved: {filename}")