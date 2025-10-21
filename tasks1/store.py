import json
import sys
import os

DATA_FILE = "tasks.json"

def load_tasks():
	if not os.path.exists(DATA_FILE):
		return []
	with open(DATA_FILE, "r") as f:
		return json.load(f)

def save_tasks(tasks):
	with open(DATA_FILE, "w") as f:
		json.dump(tasks, f, indent=2)

def main():
	if len(sys.argv) < 2:
		print("Usage: python store.py <task description>")
		return
	task_desc = " ".join(sys.argv[1:])
	tasks = load_tasks()
	tasks.append({"description": task_desc})
	save_tasks(tasks)
	print(f"Task added: {task_desc}")

if __name__ == "__main__":
	main()
