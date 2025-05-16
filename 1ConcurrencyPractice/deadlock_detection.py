"""
A deadlock happens when:

Two (or more) threads/processes are waiting on each other

And none can proceed, because they're all holding resources the others need

Classic Example:
🧵 Thread A holds Lock 1, wants Lock 2

🧵 Thread B holds Lock 2, wants Lock 1

They both wait forever → 💥 Deadlock
"""

# Solution 1: Resource Allocation Graph - Build a graph of resources and processes - Detect cycles
# Solution 2: Wait-for Graph - Similar to resource allocation graph, but focuses on wait-for relationships

from collections import defaultdict

class DeadlockDetector:
    def __init__(self):
        self.graph = defaultdict(set)

    def request(self, thread, resource):
        """Thread is waiting for resource"""
        self.graph[thread].add(resource)

    def allocate(self, resource, thread):
        """Resource is held by thread"""
        self.graph[resource].add(thread)

    def release(self, resource, thread):
        """Remove edge from resource to thread"""
        if thread in self.graph[resource]:
            self.graph[resource].remove(thread)

    def grant(self, thread, resource):
        """Thread no longer waiting for resource"""
        if resource in self.graph[thread]:
            self.graph[thread].remove(resource)

    def is_deadlocked(self):
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False
