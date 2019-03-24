# Copyright 2019 Kensho Technologies, LLC.
"""Module for Wikidata JSON dumps."""
import bz2
import gzip
import json
import logging
import os
import subprocess
from contextlib import contextmanager
from typing import IO, Any, Dict, Iterator, List, Optional, Tuple


class WikidataJsonDump:
    """Class for Wikidata JSON dump files.

    Represents a json file from https://dumps.wikimedia.org/wikidatawiki/entities.
    File names are of the form "wikidata-YYYYMMDD-all.json[.bz2|.gz]".  The file is a single JSON
    array and there is one element (i.e. item or property) on each line with the first and
    last lines being the opening and closing square brackets.  This class can handle bz2 or gz
    compressed files as well as the uncompressed json files.

    Parameters
    ----------
    filename: str
      The wikidata JSON dump file name (e.g. `my_data_dir/wikidata-20180730-all.json.bz2`)
    """

    def __init__(self, filename: str) -> None:
        if not isinstance(filename, str):
            raise ValueError("filename must be a string")

        if filename.endswith(".json"):
            self.basename, _ = os.path.splitext(filename)
            self.compression = None
        elif filename.endswith((".json.bz2", ".json.gz")):
            self.basename, _ = os.path.splitext(os.path.splitext(filename)[0])
            self.compression = os.path.splitext(filename)[1]
        else:
            raise ValueError('filename must end with ".json.bz2" or ".json.gz" or ".json"')

        self.filename = filename
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def _open_dump_file(self) -> Iterator[IO[Any]]:
        """Context manager that opens compressed/uncompressed dump files.

        It is important to open the file in binary mode even if it is not compressed. This allows us
        to handle decoding in one place.
        """
        if self.compression == ".bz2":
            with bz2.open(self.filename, mode="rb") as fp:
                yield fp
        elif self.compression == ".gz":
            with gzip.open(self.filename, mode="rb") as fp:
                yield fp
        else:
            with open(self.filename, mode="rb") as fp:
                yield fp

    def iter_lines(self) -> Iterator[str]:
        """Generate lines from JSON dump file."""
        with self._open_dump_file() as fp:
            for linebytes in fp:
                yield linebytes.decode("utf-8")

    def __iter__(self) -> Iterator[Dict]:
        """Iterate over lines in the file."""
        for line_str in self.iter_lines():
            line_str = line_str.rstrip(",\n")
            # first and last lines are opening and closing brackets
            if line_str in ["[", "]"]:
                continue
            yield json.loads(line_str)

    def _write_chunk(
        self, out_fbase: str, ichunk: int, out_format: str, out_lines: List[str]
    ) -> Tuple[List[str], int, str]:
        """Write a single chunk to disk."""
        out_fname = f"{out_fbase}-ichunk_{ichunk}.{out_format}"
        self.logger.debug(f"writing {out_fname}")
        out_lines = [out_line.rstrip(",\n") for out_line in out_lines]
        with open(out_fname, "w") as fp:
            if out_format == "json":
                fp.write("[\n")
                fp.write(",\n".join(out_lines))
                fp.write("\n]\n")
            elif out_format == "jsonl":
                fp.write("\n".join(out_lines))

        if self.compression == "bz2":
            args = ["bzip2", out_fname]
            subprocess.check_output(args)
            out_fname = f"{out_fname}.bz2"
        elif self.compression == "gz":
            args = ["gzip", out_fname]
            subprocess.check_output(args)
            out_fname = f"{out_fname}.gz"

        out_lines = []
        ichunk += 1
        return out_lines, ichunk, out_fname

    def create_chunks(
        self,
        out_fbase: Optional[str] = None,
        out_format: str = "json",
        num_lines_per_chunk: int = 100,
        max_chunks: int = 10 ** 10,
    ) -> List[str]:
        """Produce N files with `num_lines_per_chunk` wikidata items per file.

        Parameters
        ----------
        out_fbase: str
          Each output file will have the form `{out_fbase}_ichunk_{ichunk}.(json|jsonl)[.bz2|.gz]`
        out_format: str
          One of ["json", "jsonl"].  If `json`, then each file is a valid json array
          (as in the original dump file).  If `jsonl`, then each file is in the
          "JSON Lines" format (http://jsonlines.org/).
        num_lines_per_chunk: int
          Number of lines per chunk file
        max_chunks: int
          Maximum number of chunks to write
        """
        wd_dump = WikidataJsonDump(self.filename)
        if out_fbase is None:
            out_fbase = self.basename

        ichunk = 0
        out_lines: List[str] = []
        out_fnames: List[str] = []

        for iline, line in enumerate(wd_dump.iter_lines()):
            if line.strip() in ["[", "]"]:
                continue
            out_lines.append(line)
            if len(out_lines) >= num_lines_per_chunk:
                out_lines, ichunk, out_fname = self._write_chunk(
                    out_fbase, ichunk, out_format, out_lines
                )
                out_fnames.append(out_fname)

            if ichunk >= max_chunks:
                return out_fnames

        if len(out_lines) > 0:
            out_lines, ichunk, out_fname = self._write_chunk(
                out_fbase, ichunk, out_format, out_lines
            )
            out_fnames.append(out_fname)

        return out_fnames

    def __str__(self) -> str:
        return "WikidataJsonDump(filename={})".format(self.filename)

    def __repr__(self) -> str:
        return self.__str__()
