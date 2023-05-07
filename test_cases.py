import pytest
import sync
import os
import hashlib


def test_source_path():

    with pytest.raises(FileNotFoundError):
        sync.main('\\wrong\\path',
                  'C:\\Users\\Pavitra\\Desktop\\Veeam\\Veeam-Python-Task\\replica', '1', 'log_new.txt')

# dest does not exist, then creating and copying


def test_copy_file(tmpdir):
    CONTENT = "Test case 3"
    source = tmpdir.join("source")
    dest = tmpdir.join("replica")
    source.mkdir()
    source_file = source / "pytest.txt"
    source_file.write_text(CONTENT, encoding='utf-8')
    sync.sync(str(source), str(dest))
    dest_file = dest / "pytest.txt"
    assert os.path.exists(dest_file)

# dest exists, compare files and copy from source to dest


def test_file_exists(tmpdir):
    CONTENT = "Test case 3"
    source = tmpdir.join("source")
    dest = tmpdir.join("replica")
    source.mkdir()
    dest.mkdir()
    source_file = source / "pytest.txt"
    source_file.write_text(CONTENT, encoding='utf-8')
    sync.sync(str(source), str(dest))
    dest_file = dest / "pytest.txt"
    assert os.path.exists(dest_file)

# dest exists - dest has file but not at source


def test_file_removal(tmpdir):
    CONTENT = "abc"
    source = tmpdir.join("source")
    dest = tmpdir.join("replica")
    source.mkdir()
    dest.mkdir()
    dest_file = dest / "abc.txt"
    dest_file.write_text(CONTENT, encoding='utf-8')
    sync.sync(str(source), str(dest))
    assert not os.path.exists(dest_file)

# source file modified and update at replica


def test_file_modification(tmpdir):
    CONTENT_source = "source content"
    CONTENT_dest = "dest content"

    source = tmpdir.join("source")
    dest = tmpdir.join("replica")
    source.mkdir()
    dest.mkdir()
    source_file = source / "abc.txt"
    dest_file = dest / "abc.txt"
    source_file.write_text(CONTENT_source, encoding='utf-8')
    dest_file.write_text(CONTENT_dest, encoding='utf-8')
    sync.sync(str(source), str(dest))
    with open(source_file, 'rb') as s:
        content = s.read()
        hash_object = hashlib.md5(content)
        md5_hash_source = hash_object.hexdigest()
    with open(dest_file, 'rb') as d:
        content = d.read()
        hash_object = hashlib.md5(content)
        md5_hash_dest = hash_object.hexdigest()
    assert md5_hash_source == md5_hash_dest

# test folder existing at source but not at replica


def test_folder(tmpdir):
    source = tmpdir.join("source")
    source.mkdir()
    extra = source.join("extra")
    dest = tmpdir.join("replica")
    extra.mkdir()
    dest.mkdir()
    sync.sync(str(source), str(dest))
    dest_dir = dest.join("extra")
    assert os.path.exists(dest_dir)

# test subdirectories existing at replica but not at source


def test_removal_folder(tmpdir):
    source = tmpdir.join("source")
    source.mkdir()
    dest = tmpdir.join("replica")
    dest.mkdir()
    extra = dest.join("extra")
    extra.mkdir()
    sync.sync(str(source), str(dest))
    assert not os.path.exists(extra)

# copy files at subdir of source


def test_folder_file(tmpdir):
    CONTENT = "subfolder text"
    source = tmpdir.join("source")
    source.mkdir()
    source_extra = source.join("extra")
    source_extra.mkdir()
    source_extra_file = source_extra / "subfolder.txt"
    source_extra_file.write_text(CONTENT, encoding='utf-8')

    dest = tmpdir.join("replica")
    dest.mkdir()

    sync.sync(str(source), str(dest))
    dest_extra = dest.join("extra")
    dest_extra_file = dest_extra / "subfolder.txt"
    assert os.path.exists(dest_extra_file)

# remove files of subdir at replica but not at source


def test_removal_folder_file(tmpdir):
    CONTENT = "subfolder dest content"
    source = tmpdir.join("source")
    source.mkdir()
    source_extra = source.join("extra")
    source_extra.mkdir()

    dest = tmpdir.join("replica")
    dest.mkdir()
    dest_extra = dest.join("extra")
    dest_extra.mkdir()
    dest_extra_file = dest_extra / "subfolder.txt"
    dest_extra_file.write_text(CONTENT, encoding='utf-8')
    sync.sync(str(source), str(dest))
    assert not os.path.exists(dest_extra_file)


def test_folder_file_modification(tmpdir):
    CONTENT_source = "Subfolder source content"
    CONTENT_dest = "Subfolder dest content"
    source = tmpdir.join("source")
    source.mkdir()
    source_extra = source.join("extra")
    source_extra.mkdir()
    source_extra_file = source_extra / "subfolder.txt"
    source_extra_file.write_text(CONTENT_source, encoding='utf-8')

    dest = tmpdir.join("replica")
    dest.mkdir()
    dest_extra = dest.join("extra")
    dest_extra.mkdir()
    dest_extra_file = dest_extra / "subfolder.txt"
    dest_extra_file.write_text(CONTENT_dest, encoding='utf-8')
    sync.sync(str(source), str(dest))
    with open(source_extra_file, 'rb') as s:
        content = s.read()
        hash_object = hashlib.md5(content)
        md5_hash_source = hash_object.hexdigest()
    with open(dest_extra_file, 'rb') as d:
        content = d.read()
        hash_object = hashlib.md5(content)
        md5_hash_dest = hash_object.hexdigest()
    assert md5_hash_source == md5_hash_dest
