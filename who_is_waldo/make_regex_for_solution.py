import re


if __name__ == "__main__":
    with open("waldo.txt", "r") as f:
        line = f.readline().rstrip("\n").split(",")
        regex = f"({'|'.join(line)})"
        regex = "^ictf{" + regex + "}$"
        # Make sure regex is valid and matches all IDs, one by one
        for id in line:
            to_check = "ictf{" + id + "}"
            assert re.match(regex, to_check)
        print(regex)
