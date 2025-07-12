#!/usr/bin/env python3
"""
Sample Python file for testing webhook triggers
"""

def hello_world():
    """Simple function to demonstrate code changes"""
    return "Hello, World!"

def add_numbers(a, b):
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    print(hello_world())
    print(f"2 + 3 = {add_numbers(2, 3)}")