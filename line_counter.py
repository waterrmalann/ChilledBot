import os

def count_lines():
    comments, coroutines, functions, classes, lines, filecount = 0, 0, 0, 0, 0, 0
    py, json = 0, 0
    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:
            filecount += 1
            if file.endswith('.json'): json += 1
            if file.endswith('.py'):
                py += 1
                with open(os.path.join(subdir, file), encoding="utf8") as f:
                    for line in f.readlines():
                        l = line.strip()
                        if l.startswith('class'): classes += 1
                        if l.startswith('def'): functions += 1
                        if l.startswith('async def'): coroutines += 1
                        if '#' in l: comments += 1
                        lines += 1
    file_dict = {
        "files": {
            "count": filecount,
            "json": json,
            "py": py
        },
        "lines": lines,
        "classes": classes,
        "functions": functions,
        "coroutines": coroutines,
        "comments": comments
    }

    return file_dict