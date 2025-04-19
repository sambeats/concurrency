import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

# ----------------------------
# 1. ASYNC FUNCTION
# ----------------------------
async def async_hello():
    print("👋 async_hello(): started")
    await asyncio.sleep(1)  # Simulate async wait
    print("✅ async_hello(): done")
    return "async_hello result"


# ----------------------------
# 2. SYNC FUNCTION (BLOCKING)
# ----------------------------
def sync_blocking_task():
    print("🧱 sync_blocking_task(): started (blocking for 2s)")
    time.sleep(2)  # This blocks!
    print("✅ sync_blocking_task(): done")
    return "sync_blocking_task result"


# ----------------------------
# 3. RUN async FUNCTION FROM SYNC CONTEXT
# ----------------------------
def call_async_from_sync():
    print("\n🔄 call_async_from_sync(): calling async_hello() using asyncio.run")
    result = asyncio.run(async_hello())  # This creates and runs an event loop
    print(f"➡️ Result: {result}")


# ----------------------------
# 4. RUN sync FUNCTION FROM async CONTEXT
# ----------------------------
async def call_sync_from_async():
    print("\n🔄 call_sync_from_async(): running sync_blocking_task() in background thread")

    loop = asyncio.get_running_loop()

    # Offload blocking task to thread executor
    result = await loop.run_in_executor(None, sync_blocking_task)

    print(f"➡️ Result: {result}")


# ----------------------------
# 5. COMBINED FUNCTION TO TEST EVERYTHING
# ----------------------------
def main():
    print("\n🎯 Example 1: Run async from sync (asyncio.run)")
    call_async_from_sync()

    print("\n🎯 Example 2: Run sync from async (run_in_executor)")
    asyncio.run(call_sync_from_async())  # We are in sync, so we run async again


# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    print("🚀 Starting async/sync demo")
    main()
    print("🏁 All done!")
