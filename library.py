import sys

def parse_line(line):
    """
    Split a line like "text goes here|123" into text and line number.
    """
    line = line.strip("\n")
    text, number = line.rsplit("|", 1)
    return text, int(number)

def process_book(filename):
    with open(filename, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    lines = []  # will hold (line_number, text)
    total_length = 0

    longest_text = ""
    longest_number = -1
    longest_length = -1

    for line in raw_lines:
        text, number = parse_line(line)
        length = len(text)
        total_length += length
        lines.append((number, text))

        # Longest line logic (break ties by larger line number)
        if length > longest_length or (length == longest_length and number > longest_number):
            longest_length = length
            longest_number = number
            longest_text = text

    # Average length (rounded)
    avg_length = round(total_length / len(lines))

    # Unscramble (sort by line number)
    lines.sort(key=lambda x: x[0])
    ordered_text = [t for _, t in lines]

    return longest_number, longest_text, avg_length, ordered_text

def write_output(input_file, longest_num, longest_text, avg_length, ordered_lines):
    code = input_file.split(".")[0]     # e.g., "TTL"
    output_file = code + "_book.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(code + "\n")
        f.write(f"Longest line ({longest_num}): {longest_text}\n")
        f.write(f"Average length: {avg_length}\n")
        for line in ordered_lines:
            f.write(line + "\n")

    print("Created:", output_file)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 library.py <filename>")
        return

    filename = sys.argv[1]

    longest_num, longest_text, avg_length, ordered = process_book(filename)
    write_output(filename, longest_num, longest_text, avg_length, ordered)

if __name__ == "__main__":
    main()
