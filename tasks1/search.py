import json
import sys
import os

DATA_FILE = "tasks.json"

def load_tasks():
	if not os.path.exists(DATA_FILE):
		return []
	with open(DATA_FILE, "r") as f:
		return json.load(f)

def main():
	if len(sys.argv) < 2:
		print("Usage: python search.py <search term>")
		return
	term = " ".join(sys.argv[1:]).lower()
	tasks = load_tasks()
	found = [task for task in tasks if term in task['description'].lower()]
	if not found:
		print("No matching tasks found.")
		return
	for i, task in enumerate(found, 1):
		print(f"{i}. {task['description']}")

if __name__ == "__main__":
	main()
