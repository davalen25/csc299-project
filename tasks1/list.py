import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
	if not os.path.exists(DATA_FILE):
		return []
	with open(DATA_FILE, "r") as f:
		return json.load(f)

def main():
	import sys
	tasks = load_tasks()
	if not tasks:
		print("No tasks found.")
		return
	for i, task in enumerate(tasks, 1):
		print(f"{i}. {task['description']}")

if __name__ == "__main__":
	main()
