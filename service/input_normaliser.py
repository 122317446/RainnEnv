# ==========================================
# File: stage0_input_normaliser.py
# Created in iteration: 3
# Author: Karl Concha
#
# Purpose:
# Handles Stage 0 of the agent pipeline:
# - Reads uploaded files (.txt / .pdf / .csv)
# - Normalises content to plain text
# - Writes initial artifact (00_input_original.txt)
#
# No DB access. No side effects outside filesystem.
# ==========================================

import os
from task_logic.file_reader import FileReader


class Stage0InputNormaliser:
    """
    Executes Stage 0: Input normalisation.
    Responsible only for file reading, cleaning, and artifact writing.
    """

    @staticmethod
    def run(file_path, run_folder, original_filename):
        """
        Reads and normalises an uploaded file and writes 00_input_original.txt

        Returns:
            plain_text (str)
            artifact_path (str)
        """

        # ------------------------------------------
        # 1) Read file using FileReader
        # ------------------------------------------
        plain_text = FileReader.read_file(file_path)

        if plain_text is None:
            raise Exception("FileReader returned no content.")

        # ------------------------------------------
        # 2) Normalisation pass
        # ------------------------------------------
        plain_text = (
            plain_text
            .replace("\r\n", "\n")
            .replace("\r", "\n")
            .strip()
        )

        if plain_text == "[Unsupported file type]":
            raise Exception(f"Unsupported file type: {original_filename}")

        if len(plain_text) == 0:
            raise Exception("No text content extracted from file.")

        # ------------------------------------------
        # 3) Write initial artifact
        # ------------------------------------------
        artifact_path = os.path.join(run_folder, "00_input_original.txt")

        with open(artifact_path, "w", encoding="utf-8") as f:
            f.write(plain_text)

        return plain_text, artifact_path
