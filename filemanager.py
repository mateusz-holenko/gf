#!/usr/bin/python3
import os

interesting_extensions = []
ignored_extensions = ['exe', 'dll', 'mdb', 'png', 'so', 'zip', 'gz', 'ttf', 'jpeg', 'jpg', 'pcap', 'o', 'a', 'nupkg', 'pdf' ]
ignored_directories = ['.git', 'Binaries', 'bin', 'fonts']

# 200 kB
maximum_file_size = 200 * 1024 * 1024

def scan(directory):
    global ignored_directories
    interesting_files = []

    for entry in os.listdir(directory):
        to_scan = []
        path = os.path.join(directory, entry)
        if os.path.isdir(path):
            if entry not in ignored_directories:
                to_scan.extend(scan(path))
        else:
            to_scan.append(path)

        for inner_entry in to_scan:
            if check(inner_entry):
                interesting_files.append(inner_entry)

    return interesting_files

def check(path):
    global interesting_extensions
    global ignored_extensions
    global maximum_file_size

    if os.stat(path).st_size > maximum_file_size:
        return False
    for ignored_extension in ignored_extensions:
        if path.endswith('.' + ignored_extension):
            return False
    if len(interesting_extensions) > 0:
        for interesting_extension in interesting_extensions:
            if path.endswith('.' + interesting_extension):
                return True
        return False
    return True

