#!/usr/bin/python
# -*- coding: utf-8 -*-
import NowPlaying # The code to test

import xml.etree.ElementTree as ET

def test_safeprint_GetsUnsafeAccentString_OutputsSafeString(capsys):
    NowPlaying.safeprint(u"caf\xe9")
    captured = capsys.readouterr()
    assert captured.out == u"café\n"

def test_safeprint_GetsUnsafeJapaneseString_OutputsSafeString(capsys):
    NowPlaying.safeprint(u"テストタイトル - 目黒 将司")
    captured = capsys.readouterr()
    assert captured.out == u"テストタイトル - 目黒 将司\n"

def test_safeprint_GetsSafeString_OutputsSafeString(capsys):
    NowPlaying.safeprint("test")
    captured = capsys.readouterr()
    assert captured.out == "test\n"

def test_unescapeString_GetsEscapedString_OutputsUnescapedString():
    escapedString = "Guns &amp; Roses - You &amp; Me"
    output = NowPlaying.unescapeString(escapedString)

    assert output == "Guns & Roses - You & Me"

def test_unescapeString_GetsUnescapedString_OutputsUnescapedString():
    escapedString = "Guns & Roses - You & Me"
    output = NowPlaying.unescapeString(escapedString)

    assert output == "Guns & Roses - You & Me"