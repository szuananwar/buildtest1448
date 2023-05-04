import os
import random
import string
import tempfile

import pytest
from buildtest.cli.inspect import inspect_cmd
from buildtest.cli.report import Report
from buildtest.defaults import BUILDTEST_ROOT
from rich.color import Color


def test_buildtest_inspect_list():
    # buildtest inspect list
    class args:
        subcommands = "inspect"
        inspect = "list"
        terse = False
        no_header = False
        builder = False
        color = Color.default().name
        pager = False

    inspect_cmd(args)

    # buildtest inspect list --pager
    class args:
        subcommands = "inspect"
        inspect = "list"
        terse = False
        no_header = False
        builder = False
        color = Color.default().name
        pager = True

    inspect_cmd(args)

    # buildtest inspect list --row-count
    class args:
        subcommands = "inspect"
        inspect = "list"
        terse = False
        no_header = False
        builder = False
        color = Color.default().name
        pager = False
        row_count = True

    inspect_cmd(args)

    # buildtest inspect list --terse --no-header
    class args:
        subcommands = "inspect"
        inspect = "list"
        terse = True
        no_header = True
        builder = False
        color = False
        pager = False

    inspect_cmd(args)

    # buildtest inspect list --terse --pager
    class args:
        subcommands = "inspect"
        inspect = "list"
        terse = True
        no_header = False
        builder = False
        color = False
        pager = True

    inspect_cmd(args)

    # buildtest inspect list --builder
    class args:
        subcommands = "inspect"
        inspect = "list"
        terse = False
        no_header = False
        builder = True
        color = False
        pager = False

    inspect_cmd(args)

    # buildtest inspect list --builder --pager
    class args:
        subcommands = "inspect"
        inspect = "list"
        terse = False
        no_header = False
        builder = True
        color = False
        pager = True

    inspect_cmd(args)


def test_buildtest_inspect_name():
    r = Report()

    # select a random test name
    test_names = r.get_random_tests(num_items=2)

    class args:
        subcommands = "inspect"
        inspect = "name"
        name = test_names
        report = None
        pager = True

    print(f"Querying test names: {args.name}")
    # buildtest inspect name <name1> <name2>
    inspect_cmd(args)

    random_test = [
        "".join(random.choices(string.ascii_letters, k=10)),
        "".join(random.choices(string.ascii_letters, k=10)),
    ]

    class args:
        subcommands = "inspect"
        inspect = "name"
        name = random_test
        report = None
        pager = False

    print(f"Querying test names: {args.name}")
    with pytest.raises(SystemExit):
        inspect_cmd(args)

    class args:
        subcommands = "inspect"
        inspect = "name"
        name = [r.builder_names()[0]]
        report = None
        pager = False

    inspect_cmd(args)


def test_buildspec_inspect_buildspec():
    tf = tempfile.NamedTemporaryFile(delete=True)

    class args:
        subcommands = "inspect"
        inspect = "buildspec"
        buildspec = [tf.name]
        report = None
        all = None
        pager = False

    # if buildspec not in cache we raise error
    with pytest.raises(SystemExit):
        inspect_cmd(args)

    # delete file
    tf.close()
    # invalid filepath will raise an error
    with pytest.raises(SystemExit):
        inspect_cmd(args)

    search_buildspec = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml"),
        os.path.join(BUILDTEST_ROOT, "tutorials", "pass_returncode.yml"),
    ]

    class args:
        subcommands = "inspect"
        inspect = "buildspec"
        buildspec = search_buildspec
        report = None
        all = False
        pager = False

    # buildtest inspect buildspec $BUILDTEST_ROOT/tutorials/vars.yml $BUILDTEST_ROOT/tutorials/pass_returncode.yml
    inspect_cmd(args)

    class args:
        subcommands = "inspect"
        inspect = "buildspec"
        buildspec = search_buildspec
        report = None
        all = True
        pager = True

    # buildtest inspect buildspec --all --pager $BUILDTEST_ROOT/tutorials/vars.yml $BUILDTEST_ROOT/tutorials/pass_returncode.yml
    inspect_cmd(args)


def test_buildtest_query():
    report = Report()
    names = report.get_names()

    class args:
        subcommands = "inspect"
        inspect = "query"
        name = names
        output = True
        error = True
        testpath = True
        buildscript = True
        buildenv = True
        theme = "emacs"
        pager = True

    # buildtest inspect query --output --error --testpath --buildscript --buildenv <name1> <name2> ...
    inspect_cmd(args)

    class args:
        subcommands = "inspect"
        inspect = "query"
        name = ["stream_test"]
        output = False
        error = False
        testpath = False
        buildscript = False
        buildenv = False
        theme = None
        pager = False

    # buildtest inspect query stream_test
    # the 'stream_test' will add coverage where metrics are printed in output of 'buildtest inspect query'
    inspect_cmd(args)

    class args:
        subcommands = "inspect"
        inspect = "query"
        name = ["".join(random.choices(string.ascii_letters, k=10))]
        report = None
        output = True
        error = False
        testpath = False
        buildscript = False
        buildenv = False
        theme = None
        pager = False

    # check invalid test name when querying result which will result in exception SystemExit
    with pytest.raises(SystemExit):
        inspect_cmd(args)
