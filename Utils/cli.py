#This file contains all cli related changes
import sys

def takeUserInput():
    if (args_count := len(sys.argv)) > 2:
        print(f"One argument expected, got {args_count - 1}")
        raise SystemExit(2)
    elif args_count < 2:
        print("You must specify the PR id")
        raise SystemExit(2)

    pull_request_id = sys.argv[1]
    return pull_request_id
