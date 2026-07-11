from parsers import parse_document

# Update these paths to point at real files on your machine
TEST_PDF = "test_files/sample.pdf"
TEST_DOCX = "test_files/sample.docx"
TEST_TXT = "test_files/sample.txt"
TEST_URL = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"

def run_test(label, file_path, file_type):
    print(f"\n--- Testing {label} ---")
    try:
        text = parse_document(file_path, file_type)
        print(f"Success. Extracted {len(text)} characters.")
        print("Preview:", text[:200])
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    run_test("PDF", TEST_PDF, "pdf")
    run_test("DOCX", TEST_DOCX, "docx")
    run_test("TXT", TEST_TXT, "txt")
    run_test("URL", TEST_URL, "url")