import pytest
from pathlib import Path
import frontmatter
import shutil
import tempfile
from datetime import datetime
import re

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

import pytest
import frontmatter
import shutil
from datetime import datetime

import mod_front_matter


@pytest.fixture
def temp_md_file(tmp_path):
    test_file = tmp_path / "test_mod_front_matter.md"
    test_file.write_text(
        "---\n"
        "title: Original Title\n"
        "date: 2024-01-01\n"
        "draft: true\n"
        "tags: [\"test\"]\n"
        "author: David\n"
        "ShowReadingTime: true\n"
        "---\n\n"
        "# Sample Content\n"
    )
    return test_file

def test_detect_format(temp_md_file):
    post = frontmatter.load(temp_md_file)
    fmt = mod_front_matter.detect_format(post.metadata)
    assert fmt == "papermod"

def test_conversion_to_astrolaunch(temp_md_file):
    post = frontmatter.load(temp_md_file)
    converted = mod_front_matter.convert_to_astrolaunch(post.metadata)
    assert converted["layout"] == "blog"
    assert converted["pageTitle"] == "Original Title"
    assert converted["publishDate"] == "2024-01-01"
    assert converted["tags"] == ["test"]
    assert converted["author"] == "David"

def test_override_and_backup(temp_md_file):
    original = temp_md_file.read_text()

    # Simulate CLI-style override
    fm = frontmatter.load(temp_md_file)
    fmt = mod_front_matter.detect_format(fm.metadata)
    if fmt == "papermod":
        fm.metadata = mod_front_matter.convert_to_astrolaunch(fm.metadata)

    overrides = [("draft", "false"), ("pageTitle", "Updated Title")]
    updated = mod_front_matter.update_or_insert(fm.metadata, overrides)

    # Write back with backup
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = temp_md_file.parent / f"_mfm_{timestamp}_{temp_md_file.name}"
    shutil.copy2(temp_md_file, backup_path)

    with open(temp_md_file, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(fm))

    assert Path(backup_path).exists()
    modified = frontmatter.load(temp_md_file)
    assert modified["draft"] is False
    assert modified["pageTitle"] == "Updated Title"

