from task_logic.file_reader import FileReader

def run_summarise(file):
    """
    Placeholder logic for summarisation task.
    Only demonstrates file reading + structure.
    Actual summarisation will be done by the AI agent later.
    """

    text = FileReader.read_file(file)

    # No real logic here! Just return text to show pipeline works.
    return f"[Summarise Task Placeholder]\n\nExtracted Text:\n{text}"
