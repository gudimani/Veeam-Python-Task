import hashlib
import os
import sync


# wrong source input should result in console output message
def test_source_path(capfd, tmpdir):

    dest = tmpdir.join("replica")
    dest.mkdir()
    sync.main('\\wrong\\path',
              str(dest), 1, 'log_new.txt')
    out, err = capfd.readouterr()
    assert out == 'Source path does not exist. Please enter valid source path.\n'

# wrong source input should result in console output message


def test_interval(capfd, tmpdir):
    source = tmpdir.join("source")
    dest = tmpdir.join("replica")
    source.mkdir()
    dest.mkdir()
    sync.main(str(source), str(dest), -1, 'log_new.txt')
    out, err = capfd.readouterr()
    assert out == 'Please provide positive interval value\n'


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

# dest exists - dest has file but not at source, so file is removed from dest


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

# File is present at both source and dest
# but when source file is modified,the file at replica is updated


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

# a subfolder existing at source but not at replica,
# the subfolder is created at replica


def test_folder(tmpdir):
    source = tmpdir.join("source")
    source.mkdir()
    subfolder = source.join("subfolder")
    dest = tmpdir.join("replica")
    subfolder.mkdir()
    dest.mkdir()
    sync.sync(str(source), str(dest))
    dest_dir = dest.join("subfolder")
    assert os.path.exists(dest_dir)

# test subfolder existing at replica but not at source,
# subfolder is removed from replica


def test_removal_folder(tmpdir):
    source = tmpdir.join("source")
    source.mkdir()
    dest = tmpdir.join("replica")
    dest.mkdir()
    subfolder = dest.join("subfolder")
    subfolder.mkdir()
    sync.sync(str(source), str(dest))
    assert not os.path.exists(subfolder)

# when new file created at source in a subfolder,
# create the same file in replica


def test_folder_file(tmpdir):
    CONTENT = "subfolder text"
    source = tmpdir.join("source")
    source.mkdir()
    source_subfolder = source.join("subfolder")
    source_subfolder.mkdir()
    source_subfolder_file = source_subfolder / "subfolder.txt"
    source_subfolder_file.write_text(CONTENT, encoding='utf-8')
    dest = tmpdir.join("replica")
    dest.mkdir()
    sync.sync(str(source), str(dest))
    dest_subfolder = dest.join("subfolder")
    dest_subfolder_file = dest_subfolder / "subfolder.txt"
    assert os.path.exists(dest_subfolder_file)

# remove files present in a subfolder at replica but not at source


def test_removal_folder_file(tmpdir):
    CONTENT = "subfolder dest content"
    source = tmpdir.join("source")
    source.mkdir()
    source_subfolder = source.join("subfolder")
    source_subfolder.mkdir()

    dest = tmpdir.join("replica")
    dest.mkdir()
    dest_subfolder = dest.join("subfolder")
    dest_subfolder.mkdir()
    dest_subfolder_file = dest_subfolder / "subfolder.txt"
    dest_subfolder_file.write_text(CONTENT, encoding='utf-8')
    sync.sync(str(source), str(dest))
    assert not os.path.exists(dest_subfolder_file)

# a file present in a subfolder at source is modified should be updated in replica


def test_folder_file_modification(tmpdir):
    CONTENT_source = "Subfolder source content"
    CONTENT_dest = "Subfolder dest content"
    source = tmpdir.join("source")
    source.mkdir()
    source_subfolder = source.join("subfolder")
    source_subfolder.mkdir()
    source_subfolder_file = source_subfolder / "subfolder.txt"
    source_subfolder_file.write_text(CONTENT_source, encoding='utf-8')
    dest = tmpdir.join("replica")
    dest.mkdir()
    dest_subfolder = dest.join("subfolder")
    dest_subfolder.mkdir()
    dest_subfolder_file = dest_subfolder / "subfolder.txt"
    dest_subfolder_file.write_text(CONTENT_dest, encoding='utf-8')
    sync.sync(str(source), str(dest))
    with open(source_subfolder_file, 'rb') as s:
        content = s.read()
        hash_object = hashlib.md5(content)
        md5_hash_source = hash_object.hexdigest()
    with open(dest_subfolder_file, 'rb') as d:
        content = d.read()
        hash_object = hashlib.md5(content)
        md5_hash_dest = hash_object.hexdigest()
    assert md5_hash_source == md5_hash_dest
