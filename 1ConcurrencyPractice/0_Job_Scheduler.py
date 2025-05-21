from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Set, List, Callable

# Dummy Job type: here, a callable with no args returning None
Job = Callable[[], None]

def job_scheduler(get_next_jobs, max_workers=8):
    """
    Runs jobs as soon as their dependencies are met, concurrently.

    Args:
        get_next_jobs: function(finished_jobs: set) -> list of jobs ready to run
        max_workers: max concurrency level
    """

    finished_jobs = set()
    all_jobs_done = False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while not all_jobs_done:
            ready_jobs = get_next_jobs(finished_jobs)
            if not ready_jobs:
                # No more jobs ready
                all_jobs_done = True
                continue

            # Submit all ready jobs concurrently
            futures = {executor.submit(job): job for job in ready_jobs}

            # Wait for all to finish
            for future in as_completed(futures):
                try:
                    future.result()  # will raise if job errored
                    finished_jobs.add(futures[future])
                except Exception as e:
                    print(f"Job {futures[future]} failed with error: {e}")
                    # Depending on policy: fail fast or continue
                    # Here we continue to schedule remaining jobs

        print("All jobs completed.")


# ===== Example usage =====

# Mock job class for demo
class DemoJob:
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print(f"Running job {self.name}")
        import time
        time.sleep(0.1)

    def __repr__(self):
        return f"Job({self.name})"


def demo_get_next_jobs(finished: Set[Job]) -> List[Job]:
    """
    Mock get_next_jobs for dependency graph:

    A, B have no deps
    C depends on A
    D depends on B, C
    E depends on D

    Jobs: A, B, C, D, E
    """

    jobs = {
        'A': DemoJob('A'),
        'B': DemoJob('B'),
        'C': DemoJob('C'),
        'D': DemoJob('D'),
        'E': DemoJob('E'),
    }

    # Dependency map (job name -> set of dependency job names)
    deps = {
        'A': set(),
        'B': set(),
        'C': {'A'},
        'D': {'B', 'C'},
        'E': {'D'},
    }

    finished_names = {job.name for job in finished}
    ready = []
    for name, job in jobs.items():
        if job in finished:
            continue
        if deps[name].issubset(finished_names):
            ready.append(job)
    return ready


if __name__ == "__main__":
    job_scheduler(demo_get_next_jobs)
