def parse_tasks_from_response(response_text):
    tasks = []
    for line in response_text.split('\n'):
        line = line.strip()
        if line.startswith('- ') or line.startswith('* '):
            task = line[2:].strip()
            if len(task) > 3:
                tasks.append(task)
    return tasks
