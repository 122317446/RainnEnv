from task_logic.file_reader import FileReader   # adjust filename if needed
import os

# List of test files
test_files = [
    "test_csv.csv",
    "test_file.txt",
    "test_pdf.pdf"
]

def run_tests():
    print("=== Running FileReader Tests ===\n")

    for file in test_files:
        if not os.path.exists(file):
            print(f"[ERROR] {file} not found in directory.\n")
            continue

        print(f"--- Testing {file} ---")

        try:
            content = FileReader.read(file)

            # Print first 300 characters so output is readable
            if isinstance(content, str):
                printable = content[:300].replace("\n", " ")
                print(f"Output preview: {printable}...\n")
            else:
                print("Output not a string.\n")

        except Exception as e:
            print(f"[ERROR] Exception occurred while testing {file}: {e}\n")

    print("=== Tests Completed ===")

if __name__ == "__main__":
    run_tests()
