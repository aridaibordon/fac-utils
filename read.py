import numpy as np

from pandas import DataFrame


def read_lev(path_to_file: str) -> DataFrame:
    """Read FAC energy level file as pandas dataframe."""
    LEV_HEADER_SIZE = 12

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
    for ldata in file_data[LEV_HEADER_SIZE:]:
        sdata = ldata.split()

        for ind, k in enumerate(kdata.keys()):
            data[k].append(sdata[ind])

    return DataFrame(data).astype(kdata)


def read_tr(path_to_file: str) -> DataFrame:
    """Read FAC transition file as pandas dataframe."""
    TR_HEADER_SIZE = 13

    with open(path_to_file, "r") as f:
        file_data = []
        for line in f:
            file_data.append(line)

    # The shape of tr files can change.
    dshape = len(file_data[TR_HEADER_SIZE].split())
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
    for ldata in file_data[TR_HEADER_SIZE:]:
        sdata = ldata.split()

        for ind, k in enumerate(kdata.keys()):
            data[k].append(sdata[ind])

    return DataFrame(data).astype(kdata)


def read_pi(path_to_file: str) -> DataFrame:
    """Read FAC photoionization and radiative recombination file"""
    HEADER_SIZE = 31

    def get_formatted_pi_data(raw_row: list):
        low, low2J, upp, upp2J, deltaE, _ = raw_row[0].split()
        egrid, cross_rr, cross_pi, _ = np.asarray(
            [item.split() for item in raw_row[2:]]
        ).T

        return low, low2J, upp, upp2J, deltaE, egrid, cross_rr, cross_pi

    with open(path_to_file, "r") as f:
        [f.readline() for _ in range(HEADER_SIZE)]

        raw_data = [line.strip() for line in f.readlines()]

    kdata = {
        "low": int,
        "low2J": int,
        "upp": int,
        "upp2J": int,
        "deltaE": float,
        "egrid": object,
        "cross_rr": object,
        "cross_pi": object,
    }
    data = [get_formatted_pi_data(raw_row) for raw_row in np.reshape(raw_data, (-1, 8))]

    return DataFrame(data, columns=kdata.keys()).astype(kdata)
