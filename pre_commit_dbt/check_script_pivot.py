import argparse
import re
from pathlib import Path
from typing import Generator
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple

from pre_commit_dbt.utils import add_filenames_args
from pre_commit_dbt.utils import red

REGEX_COMMENTS = r"(?<=(\/\*|\{#))((.|[\r\n])+?)(?=(\*+\/|#\}))|[ \t]*--.*"
REGEX_SPLIT = r"[\s]+"
REGEX_PARENTHESIS = r"([\(\)])"  # pragma: no mutate


def replace_comments(sql: str) -> str:
    return re.sub(REGEX_COMMENTS, "", sql)


def add_space_to_parenthesis(sql: str) -> str:
    return re.sub(REGEX_PARENTHESIS, r" \1 ", sql)


def check_pivot(sql: str) -> int:
    status_code = 0
    
    sql_clean = replace_comments(sql)
    sql_clean = add_space_to_parenthesis(sql_clean)
    sql_split = re.split(REGEX_SPLIT, sql_clean)

    if sql_split.find('PIVOT') != -1:
        status_code = 1
    
    return status_code


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)

    args = parser.parse_args(argv)
    status_code = 0

    for filename in args.filenames:
        sql = Path(filename).read_text()
        status_code_file = check_pivot(
            sql, filename
        )

        if status_code_file:
            result = "\n- ".join(list(tables))  # pragma: no mutate

            print(
                f"{red(filename)}: contains the PIVOT() function. "
                f"Datafold does not support that."
            )

            status_code = status_code_file

    return status_code


if __name__ == "__main__":
    exit(main())
