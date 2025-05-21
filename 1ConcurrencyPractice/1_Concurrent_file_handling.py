"""
Problem Statement
Design and implement a high-performance multithreaded copy(src_path, dst_path) function in Python using low-level I/O primitives:

open(filepath): Opens the file for reading/writing.

close(filepath): Closes the file.

read(buffer: bytearray, offset: int): Reads len(buffer) bytes from given offset into the buffer. Raises EOL exception on end-of-file.

write(buffer: bytearray, offset: int): Writes len(buffer) bytes from given offset. Raises WriteError on failure.

The system must:

Handle large files efficiently using multiple threads.

Maintain data integrity and correctness across threads.

Handle all I/O errors gracefully.

Use optimal buffer sizes.

Allow high throughput during file copy operations (e.g., HDD → SSD).

Follow-up Qs:

What is the bottleneck in this system?

How should the buffer size be chosen and what factors influence it?
"""
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class FileWrapper:
    def __init__(self, filepath, mode):
        self.file = open(filepath, mode + 'b')
        self.lock = threading.Lock()  # To make seek/read/write thread safe

    def close(self):
        with self.lock:
            self.file.close()

    def read(self, buffer: bytearray, offset: int) -> int:
        with self.lock:
            self.file.seek(offset)
            data = self.file.read(len(buffer))
            if not data:
                raise EOFError("EOL reached")
            buffer[:len(data)] = data
            return len(data)

    def write(self, buffer: bytearray, offset: int) -> int:
        with self.lock:
            self.file.seek(offset)
            written = self.file.write(buffer)
            if written != len(buffer):
                raise IOError("Failed to write all bytes")
            self.file.flush()
            return written


def copy(source_path: str, destination_path: str, buffer_size=64*1024, max_workers=4):
    src = FileWrapper(source_path, 'r')
    dest = FileWrapper(destination_path, 'w')

    try:
        file_size = os.path.getsize(source_path)
        dest.file.truncate(file_size)  # Pre-allocate destination size

        total_chunks = (file_size + buffer_size - 1) // buffer_size

        def copy_chunk(chunk_index):
            offset = chunk_index * buffer_size
            chunk_len = min(buffer_size, file_size - offset)
            buffer = bytearray(chunk_len)

            bytes_read = src.read(buffer, offset)
            bytes_written = dest.write(buffer[:bytes_read], offset)
            return f"Chunk {chunk_index} copied"

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(copy_chunk, i) for i in range(total_chunks)]

            for future in as_completed(futures):
                try:
                    result = future.result()
                    # Optionally print or log result
                    # print(result)
                except Exception as e:
                    # Handle exceptions from threads
                    raise RuntimeError(f"Error copying chunk: {e}")

        print("Copy successful!")

    finally:
        src.close()
        dest.close()


if __name__ == "__main__":
    copy("source.bin", "dest.bin")
