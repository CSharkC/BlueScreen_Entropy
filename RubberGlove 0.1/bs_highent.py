import bs_entropy, bs_dirscanner

def scan(path, threshold):
    expected_extentions = ('.arc', '.arj', '.as', '.b64', '.btoa', '.bz\t.cab', '.cpt', '.gz', '.hqx', '.iso', '.lha', '.lzh', '.mim', '.mme', '.pak', '.pf', '.rar', '.rpm', '.sea', '.sit', '.sitx', '.tar.gz', '.tbz', '.tbz2', '.tgz', '.uu', '.uue', '.z', '.zip', '.zipx', '.zoo', '.png', '.exe')
    expected = []
    unexpected = []
    error_files = []
    files = bs_dirscanner.get_file_list(path)
    file_len = len(files)
    for file in files:
        print(file)
        if file.endswith(expected_extentions) is False:
            try:
                entropy = bs_entropy.quick(file)
            except MemoryError:
                error_files.append([file, "Too large"])
                continue
            except PermissionError:
                error_files.append([file, "Permission Denied"])
                continue
            if entropy > threshold:
                unexpected.append([file, entropy])
        else:
            expected.append([file])
    unexpected = (sorted(unexpected,key=lambda l:l[1], reverse=True))
    return unexpected, expected, error_files
