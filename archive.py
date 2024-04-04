def delete_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def print_loading():
    loading = "...".rjust(60)
    print(loading)