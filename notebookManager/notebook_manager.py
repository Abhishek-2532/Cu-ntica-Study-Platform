import os
import json
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from config.config import NOTEBOOKS_DIR


class NotebookManager:
    @staticmethod
    def create_empty_notebook():
        return {
            "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {
                "language_info": {
                    "name": "python",
                    "version": "3.x"
                }
            },
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": "# Welcome to Flask Jupyter Notebook\n# Write Python code here and press Shift+Enter to run\nprint('Hello Jupyter!')"
                }
            ]
        }

    @staticmethod
    def parse_ipynb(content_dict):
        """Parse raw nbformat JSON dictionary into web-friendly structure."""
        cells = []
        raw_cells = content_dict.get("cells", [])

        for idx, c in enumerate(raw_cells):
            cell_type = c.get("cell_type", "code")
            source = c.get("source", "")
            if isinstance(source, list):
                source = "".join(source)

            cell_obj = {
                "id": f"cell_{idx+1}",
                "cell_type": cell_type,
                "source": source,
                "execution_count": c.get("execution_count"),
                "outputs": []
            }

            # Normalize existing outputs if present
            raw_outputs = c.get("outputs", [])
            for out in raw_outputs:
                output_type = out.get("output_type")
                if output_type == "stream":
                    text = out.get("text", "")
                    if isinstance(text, list):
                        text = "".join(text)
                    cell_obj["outputs"].append({
                        "type": "stream",
                        "name": out.get("name", "stdout"),
                        "text": text
                    })
                elif output_type in ("execute_result", "display_data"):
                    data = out.get("data", {})
                    if "image/png" in data:
                        img_data = data["image/png"]
                        if isinstance(img_data, list):
                            img_data = "".join(img_data)
                        cell_obj["outputs"].append({
                            "type": "image",
                            "mime": "image/png",
                            "data": f"data:image/png;base64,{img_data}"
                        })
                    elif "text/html" in data:
                        html = data["text/html"]
                        if isinstance(html, list):
                            html = "".join(html)
                        cell_obj["outputs"].append({"type": "html", "data": html})
                    elif "text/plain" in data:
                        txt = data["text/plain"]
                        if isinstance(txt, list):
                            txt = "".join(txt)
                        cell_obj["outputs"].append({"type": "text", "data": txt})
                elif output_type == "error":
                    tb = out.get("traceback", [])
                    cell_obj["outputs"].append({
                        "type": "error",
                        "ename": out.get("ename", "Error"),
                        "evalue": out.get("evalue", ""),
                        "raw": "\n".join(tb) if isinstance(tb, list) else str(tb)
                    })

            cells.append(cell_obj)

        return cells

    @staticmethod
    def export_ipynb(cells_data):
        """Export cells data list to standard Jupyter Notebook dict format."""
        nb = new_notebook()
        nb_cells = []

        for cell in cells_data:
            c_type = cell.get("cell_type", "code")
            source = cell.get("source", "")

            if c_type == "markdown":
                nb_cells.append(new_markdown_cell(source))
            else:
                exec_count = cell.get("execution_count")
                n_cell = new_code_cell(source)
                if exec_count is not None:
                    n_cell["execution_count"] = int(exec_count)
                nb_cells.append(n_cell)

        nb["cells"] = nb_cells
        return nb

    @staticmethod
    def list_saved_notebooks():
        if not os.path.exists(NOTEBOOKS_DIR):
            return []
        files = [f for f in os.listdir(NOTEBOOKS_DIR) if f.endswith(".ipynb")]
        return sorted(files)

    @staticmethod
    def save_notebook_to_file(filename, cells_data):
        if not filename.endswith(".ipynb"):
            filename += ".ipynb"
        path = os.path.join(NOTEBOOKS_DIR, filename)
        nb_dict = NotebookManager.export_ipynb(cells_data)
        with open(path, "w", encoding="utf-8") as f:
            nbformat.write(nbformat.from_dict(nb_dict), f)
        return path

    @staticmethod
    def load_notebook_from_file(filename):
        if not filename.endswith(".ipynb"):
            filename += ".ipynb"
        path = os.path.join(NOTEBOOKS_DIR, filename)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        return NotebookManager.parse_ipynb(nb)
