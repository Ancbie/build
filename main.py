#!/bin/env python3
import os
#Step 1 - install packages
class Builder:
    def __init__(self):
        self.apt_packages = ['libasound2-dev', 'libavcodec-dev', 'libcap-dev', 'libdrm-dev', 'libglib2.0-dev', 'libgtk-4-dev', 'libgudev-1.0-dev', 'libopenxr-dev', 'libportal-dev', 'libsqlite3-dev', 'libwebkitgtk-6.0-dev']

    def install_packages(self):

