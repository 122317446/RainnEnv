# ==========================================
# File: input_normaliser.py
# Created in iteration: 3
# Author: Karl Concha
#
# - Read uploaded file (.txt / .pdf / .csv)
# - NORMALISE extracted content to plain text for AI model to read
# - Write initial artifact: 00_input_original.txt
# 
# #ChatGPT (OpenAI, 2025) – Assisted in structuring the Stage 0 input
# normalisation process, defining the plain-text contract, and enforcing
# artifact persistence (00_input_original.txt) for traceability.
# Conversation Topic: "Input Normalisation and Artifact outputs"
# Date: January 2026
# Used in agent_runtime_servcice.py
# ==========================================

import os
from task_logic.file_reader import FileReader


class Stage0InputNormaliser:
    """
    Stage 0 (Input) handler: read → normalise → persist as artifact.

    Why this exists:
    - Supervisor feedback for Iteration 3 required that each stages working data
      is persisted in files for traceability/reporting, with choice to delete after.
    """

    @staticmethod
    def run(file_path, run_folder, original_filename):
        """
        Reads and normalises an uploaded file and writes 00_input_original.txt.
        """

        return Stage0InputNormaliser.run_multi(
            files=[{"path": file_path, "name": original_filename}],
            run_folder=run_folder
        )

    @staticmethod
    def run_multi(files, run_folder):
        """
        Reads and normalises multiple uploaded files and writes 00_input_original.txt.
        Each file is separated with a clear header for traceability.
        """
        if not files:
            raise Exception("No files provided for input normalisation.")

        combined_parts = []

        for idx, item in enumerate(files, start=1):
            file_path = item.get("path")
            file_name = item.get("name") or f"file_{idx}"

            # 1) Read file using FileReader (handles pdf/txt/csv)
            plain_text = FileReader.read_file(file_path)
            if plain_text is None:
                raise Exception("FileReader returned no content.")

            # 2) Normalisation pass (stable formatting for subsequent stages)
            plain_text = (
                plain_text
                .replace("\r\n", "\n")
                .replace("\r", "\n")
                .strip()
            )

            # If FileReader can’t handle the type, it returns a debug text
            if plain_text == "[Unsupported file type]":
                raise Exception(f"Unsupported file type: {file_name}")

            if len(plain_text) == 0:
                raise Exception(f"No text content extracted from file: {file_name}")

            combined_parts.append(f"=== FILE {idx}: {file_name} ===\n{plain_text}")

        combined_text = "\n\n".join(combined_parts).strip()

        # 3) Write stage-0 artifact
        artifact_path = os.path.join(run_folder, "00_input_original.txt")
        with open(artifact_path, "w", encoding="utf-8") as f:
            f.write(combined_text)

        return combined_text, artifact_path
