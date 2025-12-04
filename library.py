"""
library.py

Process a scrambled book file and create a new "<CODE>_book.txt" file with:
1. The three-letter code
2. The longest line (by character length) and its line number
3. The average line length (rounded to nearest integer)
4. All lines of the book in correct line-number order

Usage:
    python3 library.py TTL.txt
"""

import os
import sys


def parse_line(raw_line: str) -> tuple[str, int]:
    """
    Parse a line of the form "text|number" into (text, line_number).

    The input line may end with a newline; we strip it off.

    >>> parse_line("Hello world|10\\n")
    ('Hello world', 10)
    >>> parse_line("Just text|1")
    ('Just text', 1)
    """
    raw_line = raw_line.rstrip("\n")
    # rsplit with maxsplit=1 so only the last '|' is used
    text, number_str = raw_line.rsplit("|", 1)
    line_number = int(number_str)
    return text, line_number


def read_book_file(path: str) -> list[tuple[int, str]]:
    """
    Read the book file and return a list of (line_number, text) tuples.

    Empty lines (if any) are skipped.

    >>> rows = read_book_file("test_sample.txt")  # doctest: +SKIP
    >>> isinstance(rows, list)                    # doctest: +SKIP
    True
    """
    rows: list[tuple[int, str]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                # skip completely blank lines
                continue
            text, num = parse_line(line)
            rows.append((num, text))
    return rows


def find_longest_line(rows: list[tuple[int, str]]) -> tuple[int, str, int]:
    """
    Given a list of (line_number, text) tuples, return a tuple:
        (line_number, text, length)

    If multiple lines have the same maximum length, the line with the
    *larger line number* wins (the one that appears later in the book).

    >>> rows = [(1, "hi"), (2, "hello"), (3, "hello")]
    >>> find_longest_line(rows)
    (3, 'hello', 5)
    """
    best_line_number = -1
    best_text = ""
    best_length = -1

    for line_number, text in rows:
        current_length = len(text)
        if current_length > best_length:
            best_length = current_length
            best_line_number = line_number
            best_text = text
        elif current_length == best_length and line_number > best_line_number:
            # Same length but appears later in the book
            best_line_number = line_number
            best_text = text

    return best_line_number, best_text, best_length


def average_line_length(rows: list[tuple[int, str]]) -> int:
    """
    Compute the average length of all lines (using the text part only),
    and return it rounded to the nearest integer.

    Rounding rule: classic "round half up" using int(x + 0.5).

    >>> rows = [(1, "abcd"), (2, "ab")]
    >>> average_line_length(rows)
    3
    """
    if not rows:
        return 0

    total_chars = sum(len(text) for _, text in rows)
    count = len(rows)
    avg = total_chars / count
    return int(avg + 0.5)


def sort_lines_by_number(rows: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """
    Return a new list of (line_number, text) sorted by line_number ascending.

    >>> sort_lines_by_number([(5, "x"), (2, "y"), (3, "z")])
    [(2, 'y'), (3, 'z'), (5, 'x')]
    """
    return sorted(rows, key=lambda pair: pair[0])


def make_output_filename(input_path: str) -> tuple[str, str]:
    """
    Given the input path (e.g. 'TTL.txt' or 'books/TTL.txt'),
    return (code, output_path) where:

        code = 'TTL'
        output_path = 'TTL_book.txt' (in the same directory as input)

    >>> make_output_filename("TTL.txt")
    ('TTL', 'TTL_book.txt')
    >>> make_output_filename("books/ALG.txt")
    ('ALG', os.path.join("books", "ALG_book.txt"))
    """
    directory = os.path.dirname(input_path)
    base = os.path.basename(input_path)
    code, _ext = os.path.splitext(base)
    out_name = f"{code}_book.txt"
    if directory:
        out_path = os.path.join(directory, out_name)
    else:
        out_path = out_name
    return code, out_path


def write_output_file(
    code: str,
    output_path: str,
    longest_line_number: int,
    longest_text: str,
    average_length_value: int,
    sorted_rows: list[tuple[int, str]],
) -> None:
    """
    Write the results to the output file in the required format:

    1. book code
    2. longest line in the format: Longest line (<line_number>): <text>
    3. average length: Average length: <number>
    4+. all lines of the book in correct order, text only
    """
    with open(output_path, "w", encoding="utf-8") as f:
        # First 3 lines (metadata)
        f.write(f"{code}\n")
        f.write(f"Longest line ({longest_line_number}): {longest_text}\n")
        f.write(f"Average length: {average_length_value}\n")

        # Remaining lines: book content in order, text only
        for _, text in sorted_rows:
            f.write(text + "\n")


def process_book(input_path: str) -> None:
    """
    High-level function that ties everything together:
      - reads the book file
      - computes statistics
      - writes the output file
    """
    rows = read_book_file(input_path)

    # Compute required values
    longest_num, longest_text, _ = find_longest_line(rows)
    avg_len = average_line_length(rows)
    sorted_rows = sort_lines_by_number(rows)

    code, output_path = make_output_filename(input_path)

    write_output_file(
        code=code,
        output_path=output_path,
        longest_line_number=longest_num,
        longest_text=longest_text,
        average_length_value=avg_len,
        sorted_rows=sorted_rows,
    )


def main(argv: list[str] | None = None) -> None:
    """
    Command-line entry point.

    Expects exactly one argument: the input .txt file.

    Example:
        python3 library.py TTL.txt
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) != 1:
        print("Usage: python3 library.py BOOK_FILE.txt")
        sys.exit(1)

    input_path = argv[0]

    if not os.path.exists(input_path):
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    process_book(input_path)


if __name__ == "__main__":
    main()
