import sys

def print_error(message):    
    print(f"\033[91m[ERROR]\033[0m {message}", file=sys.stderr)

def print_example(message):
   print(f"\033[92m[EXAMPLE]\033[0m {message}", file=sys.stderr) 