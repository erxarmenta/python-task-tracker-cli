import argparse
import jsonManager
from datetime import datetime
from tabulate import tabulate

def searchByID(id: int):
    data = jsonManager.read_json()
    for t in data:
        if t['id'] == id:
            task = t
        else:
            task = None
    return task

def getDate():
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return date

def tasks(args):
    data = jsonManager.read_json()
    if len(data) < 1:
        print('There are no pending tasks')
        return
    table_data = []
    table_data.append(['ID', 'Description', 'Status', 'Created At', 'Updated At'])
    for task in data:
        aux = [task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt']]
        table_data.append(aux)
    print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))

def addTask(args):
    if args is None:
        print('You must write a description for the task')
        return
    try:
        data = jsonManager.read_json()
        newID = len(data) + 1
        date = getDate()
        newTask = {
            "id": newID,
            "description": args.description,
            "status": "todo",
            "createdAt": date,
            "updatedAt": ""
        }
        data.append(newTask)
        jsonManager.write_json(data)
        print (f"Task added successfully (ID: {newID})")
    except Exception as e:
        print(f"An error has ocurred: {e}")

def delete(args):
    if args is None:
        print('You must write an ID')
        return
    try:
        data = jsonManager.read_json()
        task = searchByID(args.id)
        if task is not None:
            data.remove(task)
            jsonManager.write_json(data)
            print('Task deleted')
        else:
            print('Task not found')
    except Exception as e:
        print(f"An error has ocurred: {e}")

def update(args):
    data = jsonManager.read_json()
    item = next((t for t in data if t['id'] == args.id), None)
    if not item:
        print(f'Task with ID {id} not found')
    else:
        if args.task is not None:
            item['description'] = args.task
            item['updatedAt'] = getDate()
        jsonManager.write_json(data)
        print(f'Task with ID {args.id} has been updated')

def main():
    parser = argparse.ArgumentParser(description = "Task Tracker CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    parser_add = subparsers.add_parser('add', help = "Add a new task")
    parser_add.add_argument('description', type=str, help="Task description")
    parser_add.set_defaults(func = addTask)

    parser_tasks = subparsers.add_parser('tasks', help = "List all tasks")
    parser_tasks.set_defaults(func = tasks)

    parser_delete = subparsers.add_parser('delete', help="Delete a task")
    parser_delete.add_argument('id', type=int, help="Task ID")
    parser_delete.set_defaults(func = delete)

    parser_update = subparsers.add_parser('update', help="Update a task")
    parser_update.add_argument('id', type=int, help="Task ID")
    parser_update.add_argument('--task', type=str, help="New task description")
    parser_update.set_defaults(func = update)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

if __name__ == '__main__':
    main()