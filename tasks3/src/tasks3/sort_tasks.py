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

def sort_alphabetical(tasks):
	"""Sort tasks alphabetically by description"""
	return sorted(tasks, key=lambda x: x['description'].lower())

def sort_by_recent(tasks):
	"""Sort tasks by most recently created (uses creation_time if available, otherwise maintains current order)"""
	# Tasks with creation_time come first, sorted by time (newest first)
	# Tasks without creation_time come after, in their original order
	with_time = [t for t in tasks if 'creation_time' in t]
	without_time = [t for t in tasks if 'creation_time' not in t]
	
	with_time_sorted = sorted(with_time, key=lambda x: x['creation_time'], reverse=True)
	return with_time_sorted + without_time

def sort_by_due_date(tasks):
	"""Sort tasks by due date (nearest dates first), tasks without due dates go to the end"""
	with_due = [t for t in tasks if 'due_date' in t]
	without_due = [t for t in tasks if 'due_date' not in t]
	
	with_due_sorted = sorted(with_due, key=lambda x: x['due_date'])
	return with_due_sorted + without_due

def swap_tasks(tasks, pos1, pos2):
	"""Swap two tasks by their position (1-indexed)"""
	if pos1 < 1 or pos1 > len(tasks) or pos2 < 1 or pos2 > len(tasks):
		print(f"Error: Task positions must be between 1 and {len(tasks)}")
		return None
	
	if pos1 == pos2:
		print("Error: Cannot swap a task with itself")
		return None
	
	# Convert to 0-indexed
	idx1, idx2 = pos1 - 1, pos2 - 1
	tasks[idx1], tasks[idx2] = tasks[idx2], tasks[idx1]
	return tasks

def display_tasks(tasks):
	"""Display tasks with their current order"""
	for i, task in enumerate(tasks, 1):
		status = task.get('status', 'not started')
		print(f"{i}. [{status.upper()}] {task['description']}")
		if 'due_date' in task:
			print(f"   Due: {task['due_date']}")
		if 'note' in task:
			print(f"   Note: {task['note']}")

def main():
	if len(sys.argv) < 2:
		print("Usage: python sort_tasks.py <sort_option> [args]")
		print("\nSort options:")
		print("  alpha          - Sort alphabetically by description")
		print("  recent         - Sort by most recently created")
		print("  due            - Sort by due date (nearest first)")
		print("  swap <n1> <n2> - Swap tasks at positions n1 and n2")
		return
	
	tasks = load_tasks()
	
	if not tasks:
		print("No tasks found.")
		return
	
	option = sys.argv[1].lower()
	
	if option == "alpha":
		tasks = sort_alphabetical(tasks)
		save_tasks(tasks)
		print("Tasks sorted alphabetically:")
		display_tasks(tasks)
		
	elif option == "recent":
		tasks = sort_by_recent(tasks)
		save_tasks(tasks)
		print("Tasks sorted by most recently created:")
		display_tasks(tasks)
		
	elif option == "due":
		tasks = sort_by_due_date(tasks)
		save_tasks(tasks)
		print("Tasks sorted by due date (nearest first):")
		display_tasks(tasks)
		
	elif option == "swap":
		if len(sys.argv) < 4:
			print("Error: swap requires two task positions")
			print("Usage: python sort_tasks.py swap <position1> <position2>")
			return
		
		try:
			pos1 = int(sys.argv[2])
			pos2 = int(sys.argv[3])
		except ValueError:
			print("Error: Task positions must be integers")
			return
		
		result = swap_tasks(tasks, pos1, pos2)
		if result is not None:
			save_tasks(result)
			print(f"Swapped tasks at positions {pos1} and {pos2}:")
			display_tasks(result)
	
	else:
		print(f"Error: Unknown sort option '{option}'")
		print("Valid options: alpha, recent, due, swap")

if __name__ == "__main__":
	main()
