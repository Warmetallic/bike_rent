import json
import os
import asyncio
import aiofiles

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the 'saved_history_files' directory exists
saved_files_dir = os.path.join(script_dir, "saved_history_files")
os.makedirs(saved_files_dir, exist_ok=True)


async def save_user_history(serialized_data, user_email):
    lines = []
    for item in serialized_data:
        line = f"ID: {item['id']}, Bicycle: {item['bicycle']}, Start: {item['start_time']}, End: {item['end_time']}, Cost: {item['cost']}"
        lines.append(line)
    rental_history_text = "\n".join(lines)

    # Asynchronously save the text content to a file in 'logged_files' directory
    text_file_name = os.path.join(saved_files_dir, f"rental_history_{user_email}.txt")
    async with aiofiles.open(text_file_name, "w") as file:
        await file.write(rental_history_text)

    # Asynchronously save the JSON content to a file in 'logged_files' directory
    json_file_name = os.path.join(saved_files_dir, f"rental_history_{user_email}.json")
    async with aiofiles.open(json_file_name, "w") as file:
        await file.write(json.dumps(serialized_data, indent=4))
