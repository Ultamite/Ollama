import json
import ollama

def prompt_llm(genre, setting, characters):
    system_prompt = f"""
You are an AI game designer. Generate deep and structured game lore in JSON format. 

Input:
- Genre: {genre}
- Setting: {setting}
- Seed Characters: {characters}

Output JSON structure:
{{
    "world_lore": "...",
    "factions": [
        {{
            "name": "...",
            "description": "...",
            "motives": "...",
            "key_members": ["..."]
        }}
    ],
    "questlines": [
        {{
            "title": "...",
            "summary": "...",
            "steps": ["...", "..."]
        }}
    ],
    "dialogue_trees": [
        {{
            "character": "...",
            "tree": {{
                "greeting": "...",
                "responses": {{
                    "Option 1": "Response 1",
                    "Option 2": "Response 2"
                }}
            }}
        }}
    ]
}}
Keep the response well-formatted and usable as JSON. Avoid explanations outside of JSON.
"""

    try:
        res = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": system_prompt}]
        )
        return res["message"]["content"]
    except Exception as e:
        return json.dumps({"error": str(e)})

def main():
    print("=== AI Game Lore Generator ===")
    genre = input("Enter game genre (e.g., Post-apocalyptic RPG): ")
    setting = input("Describe the setting (e.g., flooded Earth with sky cities): ")
    characters = input("Seed characters (comma-separated names/roles): ")

    print("\nGenerating lore... please wait.\n")
    raw_output = prompt_llm(genre, setting, characters)

    try:
        lore_json = json.loads(raw_output)
    except json.JSONDecodeError:
        print("Error: Couldn't parse JSON from response. Here's raw output:\n")
        print(raw_output)
        return

    # Pretty print result
    print(json.dumps(lore_json, indent=4))

    # Save to file
    with open("game_lore_output.json", "w", encoding="utf-8") as f:
        json.dump(lore_json, f, indent=4)
    print("\n✅ Lore saved to game_lore_output.json")

if __name__ == "__main__":
    main()