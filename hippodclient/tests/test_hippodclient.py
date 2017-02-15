import os
import tempfile
import shutil
import textwrap

from unittest import TestCase

# for image generation
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


import hippodclient



URL = "http://127.0.0.1/"


def gen_rand_image():
    tmpdir = tempfile.mkdtemp()
    tmpfile = os.path.join(tmpdir, "graph.png")

    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2*np.pi*t)
    plt.plot(t, s)

    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.savefig(tmpfile)
    return tmpdir, tmpfile

def gen_snippet_file(offset):
    tmpdir = tempfile.mkdtemp()
    tmpfile = os.path.join(tmpdir, "snippet.py")
    content = """
    import sys
    import matplotlib
    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    t = np.arange(0.0, 2.0, 0.01)
    s = {} + np.sin(2*np.pi*t)
    plt.plot(t, s)

    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.savefig(sys.argv[1])
    """.format(offset)
    fd = open(tmpfile, "w")
    fd.write(textwrap.dedent(content))
    fd.close()
    return tmpdir, tmpfile


class TestHippodClient(TestCase):

    def test_is_initiable(self):
        hippodclient.Test()
        hippodclient.Container()

    def test_upload(self):
        c = hippodclient.Container()
        c.set_url(URL)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("random title")
        t.categories_set("team:bar")
        t.attachment.tags_add("foo", "bar")
        t.achievement.result = "passed"

        c.add(t)
        c.sync()

    def test_minimal_passed(self):
        c = hippodclient.Container(url=URL)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("random title for minimal example, passed")
        t.categories_set("team:foo")
        t.achievement.result = "passed"

        c.add(t)
        c.upload()

    def test_minimal_failed(self):
        c = hippodclient.Container(url=URL)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("random title for minimal example, failed")
        t.categories_set("team:foo")
        t.achievement.result = "failed"

        c.add(t)
        c.upload()

    def test_minimal_nonapplicable(self):
        c = hippodclient.Container(url=URL)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("random title for minimal example, nonapplicable")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        c.add(t)
        c.upload()

    def test_markdown_minimal(self):
        c = hippodclient.Container(url=URL)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Markdown Test")
        description = """
        # This is a first level heading

        ## Second Level Heading

        ### Third level heading

        """
        t.description_markdown_set(description)
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        c.add(t)
        c.upload()


    def test_snippet_item(self):
        c = hippodclient.Container(url=URL)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Item")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        tmp_dir, graph_path = gen_snippet_file(1)
        t.snippet_file_add(graph_path, "x-snippet-python3-matplot-png")

        c.add(t)
        c.upload()
        shutil.rmtree(tmp_dir)

    def test_snippet_multiple__item(self):
        c = hippodclient.Container(url=URL)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Item Multiple")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        tmps = []
        for i in range(10):
            tmp_dir, graph_path = gen_snippet_file(i)
            t.snippet_file_add(graph_path, "x-snippet-python3-matplot-png")
            tmps.append(tmp_dir)

        c.add(t)
        c.upload()
        for tmp_dir in tmps:
            shutil.rmtree(tmp_dir)


    def test_snippet_achievement(self):
        c = hippodclient.Container(url=URL)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Achievement")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        tmp_dir, graph_path = gen_snippet_file(1)
        t.achievement.snippet_file_add(graph_path, "x-snippet-python3-matplot-png")

        c.add(t)
        c.upload()
        shutil.rmtree(tmp_dir)


    def test_snippet_multiple_achievement(self):
        c = hippodclient.Container(url=URL)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Achievement Multiple")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        tmps = []
        for i in range(10):
            tmp_dir, graph_path = gen_snippet_file(i)
            t.achievement.snippet_file_add(graph_path, "x-snippet-python3-matplot-png")
            tmps.append(tmp_dir)

        c.add(t)
        c.upload()
        for tmp_dir in tmps:
            shutil.rmtree(tmp_dir)


    def test_mass_upload(self):
        c = hippodclient.Container(url=URL)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Mass Upload")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        c.add(t)
        for i in range(10):
            c.upload()


    def test_different_achievements(self):
        c = hippodclient.Container(url=URL)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Achievements")
        t.categories_set("team:foo")
        t.achievement.result = "passed"
        c.add(t)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Achievements")
        t.categories_set("team:foo")
        t.achievement.result = "failed"
        c.add(t)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Achievements")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        c.add(t)

        c.upload()
