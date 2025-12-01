#!/usr/bin/env python3
import sys
import re
import os
from collections import defaultdict

def analyze_i_file(file_path):
    """
    Analyzes a preprocessed C++ file (.i) to determine which included files
    contribute the most lines of code.
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    # Pattern to match preprocessor line markers
    # Format: # linenum "filename" flags
    # Example: # 1 "/usr/include/stdio.h" 1 3 4
    # Note: Sometimes flags are absent.
    line_marker_pattern = re.compile(r'^#\s+\d+\s+"([^"]+)"')

    file_counts = defaultdict(int)
    current_file = "unknown"
    total_lines = 0
    
    print(f"Reading {file_path}...")

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1
                if total_lines % 100000 == 0:
                    print(f"Processed {total_lines} lines...", end='\r')
                    
                match = line_marker_pattern.match(line)
                if match:
                    current_file = match.group(1)
                else:
                    # Check if line is not just whitespace
                    if line.strip():
                        file_counts[current_file] += 1
    except Exception as e:
        print(f"\nError analyzing file: {e}")
        return

    print(f"\nProcessing complete.")

    # Filter out empty counts and sort
    sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)

    print(f"\nAnalysis of {file_path}:")
    print(f"Total lines scanned: {total_lines}")
    print("-" * 100)
    print(f"{'Lines':<10} | {'%':<6} | {'File Path'}")
    print("-" * 100)

    # Calculate total code lines (excluding markers and empty lines)
    total_code_lines = sum(file_counts.values())
    if total_code_lines == 0:
        total_code_lines = 1 # Avoid division by zero

    for filename, count in sorted_files[:50]:  # Show top 50
        percentage = (count / total_code_lines) * 100
        print(f"{count:<10} | {percentage:6.2f} | {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_i_file.py <path_to_i_file>")
        print("Example: python3 analyze_i_file.py myfile.i")
        sys.exit(1)
    
    analyze_i_file(sys.argv[1])

