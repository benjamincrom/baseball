"""Regression test: diff two output folders and assert they are identical.

By default compares reference_test_output/ (the known-good baseline) against
test_output_2/ (the latest generated output). Override with env vars to
compare other folders:

    REFERENCE_DIR=/path/a ACTUAL_DIR=/path/b pytest test_output_regression.py
"""
import filecmp
import os

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCE_DIR = os.environ.get('REFERENCE_DIR', os.path.join(HERE, 'reference_test_output'))
ACTUAL_DIR = os.environ.get('ACTUAL_DIR', os.path.join(HERE, 'test_output_2'))


def _compare_dirs(dir1, dir2):
    """Recursively compare two directories, returning a filecmp.dirs_cmp tree."""
    return filecmp.dircmp(dir1, dir2)


def _collect_mismatches(comparison, rel_path=''):
    """Walk a dircmp tree and collect every difference as a human-readable string."""
    mismatches = []

    for name in comparison.left_only:
        mismatches.append(f'Only in {comparison.left}: {os.path.join(rel_path, name)}')

    for name in comparison.right_only:
        mismatches.append(f'Only in {comparison.right}: {os.path.join(rel_path, name)}')

    for name in comparison.funny_files:
        mismatches.append(f'Could not compare: {os.path.join(rel_path, name)}')

    _, mismatched, errors = filecmp.cmpfiles(
        comparison.left, comparison.right, comparison.common_files, shallow=False
    )
    for name in mismatched:
        mismatches.append(f'Content differs: {os.path.join(rel_path, name)}')
    for name in errors:
        mismatches.append(f'Error comparing: {os.path.join(rel_path, name)}')

    for subdir, sub_comparison in comparison.subdirs.items():
        mismatches.extend(
            _collect_mismatches(sub_comparison, os.path.join(rel_path, subdir))
        )

    return mismatches


@pytest.fixture(scope='module')
def output_dirs():
    assert os.path.isdir(REFERENCE_DIR), f'Reference directory not found: {REFERENCE_DIR}'
    assert os.path.isdir(ACTUAL_DIR), f'Actual directory not found: {ACTUAL_DIR}'
    return REFERENCE_DIR, ACTUAL_DIR


def test_output_matches_reference(output_dirs):
    reference_dir, actual_dir = output_dirs
    comparison = _compare_dirs(reference_dir, actual_dir)
    mismatches = _collect_mismatches(comparison)

    assert not mismatches, (
        f'{len(mismatches)} difference(s) between {reference_dir} and {actual_dir}:\n'
        + '\n'.join(sorted(mismatches))
    )
