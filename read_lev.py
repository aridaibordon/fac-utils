from pandas import DataFrame


def read_lev(path_to_file: str) -> DataFrame:
    """Convert FAC energy level files to pandas
    dataframe.
    """
    f = open(path_to_file, "r")

    file_data = []
    for line in f:
        file_data.append(line)

    f.close()

    kdata = {'E': float, 'P': int, 'VNL': str, '2J': int,
             'ncomplex': str, 'sname': str, 'name': str}

    data = {key: [] for key in kdata.keys()}
    for ldata in file_data[12:]:
        sdata = ldata.split()

        for ind, k in enumerate(kdata.keys()):
            data[k].append(sdata[2:][ind])

    return DataFrame(data).astype(kdata)
