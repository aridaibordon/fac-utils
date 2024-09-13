from pandas import DataFrame


def read_lev(path_to_file: str) -> DataFrame:
    """Read FAC energy level file as pandas dataframe."""
    HEADER_SIZE = 12

    with open(path_to_file, "r") as f:
        file_data = []
        for line in f:
            file_data.append(line)

    kdata = {
        "ID": int,
        "IBASE": int,
        "E": float,
        "P": int,
        "VNL": str,
        "2J": int,
        "ncomplex": str,
        "sname": str,
        "name": str,
    }

    data = {key: [] for key in kdata.keys()}
    for ldata in file_data[HEADER_SIZE:]:
        sdata = ldata.split()

        for ind, k in enumerate(kdata.keys()):
            data[k].append(sdata[ind])

    return DataFrame(data).astype(kdata)


def read_tr(path_to_file: str) -> DataFrame:
    """Read FAC transition file as pandas dataframe."""
    HEADER_SIZE = 13

    with open(path_to_file, "r") as f:
        file_data = []
        for line in f:
            file_data.append(line)

    # The shape of tr files can change.
    dshape = len(file_data[HEADER_SIZE].split())
    if dshape == 8:
        kdata = {
            "upp": int,
            "upp2J": int,
            "low": int,
            "low2J": int,
            "deltaE": float,
            "gf": float,
            "ein": float,
            "mult": float,
        }
    elif dshape == 10:
        kdata = {
            "upp": int,
            "upp2J": int,
            "low": int,
            "low2J": int,
            "deltaE": float,
            "uta": float,
            "gf": float,
            "ein": float,
            "mult": float,
        }
    else:
        raise ValueError("File not recognized")

    data = {key: [] for key in kdata.keys()}
    for ldata in file_data[HEADER_SIZE:]:
        sdata = ldata.split()

        for ind, k in enumerate(kdata.keys()):
            data[k].append(sdata[ind])

    return DataFrame(data).astype(kdata)


def get_ein_dict(tr_df: DataFrame) -> dict:
    ein_dict = {}
    for _, tr_row in tr_df.iterrows():
        upp, low, ein = int(tr_row["upp"]), int(tr_row["low"]), tr_row["ein"]
        ein_dict[f"{upp:05d}-{low:05d}"] = ein

    return ein_dict
