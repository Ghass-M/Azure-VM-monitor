import psutil

def total_cpu_usage():
    return psutil.cpu_percent(interval=1)

def total_memory_usage():
    mem = psutil.virtual_memory()
    return (mem.percent, 100 - mem.percent)

def total_disk_usage():
    disk = psutil.disk_usage("/")
    return (disk.percent, 100 - disk.percent)

def top_processes(limit=5):
    
    current_proc = []

    # Retreiving all running processes along with their details (pid, cpu usage, memory usage)
    processes = psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"])

    # Allow psutil to measure cpu_percent by calling it once to initialize it (to give the script time to retrieve performance information)
    for p in processes:
        try:
            # First call to cpu_percent() to initialize the data
            p.cpu_percent(interval=0.1)
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Now retrieve the actual process info
    processes = psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"])
    for p in processes:
        try:
            current_proc.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Sorting processes by cpu usage and memory usage
    processes_cpu = sorted(current_proc, key=lambda p: p["cpu_percent"], reverse=True)
    processes_mem = sorted(current_proc, key=lambda p: p["memory_percent"], reverse=True)

    return processes_cpu[:limit], processes_mem[:limit]

def display_stats():
    print("======= Server stats===============\n")
    cpu = total_cpu_usage()
    print(f"Total cpu usage: {cpu}%\n")

    print("------------")
    mem = total_memory_usage()
    print(f"Used RAM: {mem[0]}%\n")
    print(f"Free RAM: {mem[1]}%\n")

    print("------------")
    disk = total_disk_usage()
    print(f"Used disk space: {disk[0]}%\n")
    print(f"Free disk space: {disk[1]}%\n")

    print("------------Top 5 processes by CPU usage------------")
    processes_cpu,processes_mem = top_processes()
    for p in processes_cpu:
        print(
            f"PID: {p['pid']}    | Name:{p['name']}              | CPU: {p['cpu_percent']}%       | Memory: {p['memory_percent']:.2f}%"
        )

    print("------------Top 5 processes by memory usage---------")
    for p in processes_mem:
        print(
            f"PID: {p['pid']}    | Name: {p['name']}              | CPU: {p['cpu_percent']}%       | Memory: {p['memory_percent']:.2f}%"
        )


if __name__ == "__main__":
    display_stats()
