import json
import sys
import os
from datetime import datetime

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
		print("Usage: python store.py <task description> [--due YYYY-MM-DD] [--note \"note text\"]")
		return
	
	# Parse arguments
	args = sys.argv[1:]
	task_desc = []
	due_date = None
	note = None
	
	i = 0
	while i < len(args):
		if args[i] == "--due" and i + 1 < len(args):
			due_date = args[i + 1]
			i += 2
		elif args[i] == "--note" and i + 1 < len(args):
			note = args[i + 1]
			i += 2
		else:
			task_desc.append(args[i])
			i += 1
	
	task_desc = " ".join(task_desc)
	
	if not task_desc:
		print("Error: Task description cannot be empty")
		return
	
	tasks = load_tasks()
	task = {
		"description": task_desc,
		"status": "not started",
		"creation_time": datetime.now().isoformat()
	}
	
	if due_date:
		task["due_date"] = due_date
	if note:
		task["note"] = note
	
	tasks.append(task)
	save_tasks(tasks)
	print(f"Task added: {task_desc}")
	if due_date:
		print(f"  Due date: {due_date}")
	if note:
		print(f"  Note: {note}")

if __name__ == "__main__":
	main()
