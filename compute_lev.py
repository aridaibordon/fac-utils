import re
import os

from pfac import fac


DEFAULT_PATH = "data/fac"


def default_file_name(elem, energy_scheme, ci_level) -> str:
    """Return default name for an energy level file"""
    if ci_level == -1:
        return f"{elem}_{energy_scheme}_NOCI.lev"
    return f"{elem}_{energy_scheme}_{ci_level}.lev"


def remove_binary_files(path):
    """Remove binary files (.b) in path"""
    for file in os.listdir(path):
        if not re.search(".b", file):
            continue
        os.remove(f"{path}/{file}")


def compute_lev(
    e_config: list[str],
    energy_scheme: str = "RDCA",
    ci_level: int = 0,
    path: str = "",
    elem: str = "K",
) -> None:
    """Compute energy levels for a given element
    and electron configuration.
    """
    fac.SetAtom(elem)
    fac.SetCILevel(ci_level)

    if energy_scheme == "RDCA":
        fac.SetUTA(1)
    elif energy_scheme == "FS":
        fac.SetUTA(0)

    glist = []
    for ind, config in enumerate(e_config):
        fac.Config(config, group=f"n{ind}")
        glist.append(f"n{ind}")
    
    fac.ConfigEnergy(0)
    fac.OptimizeRadial("n1")
    fac.ConfigEnergy(1)

    if path == "":
        path = DEFAULT_PATH

    fname = f"{path}/{default_file_name(elem, energy_scheme, ci_level)}"

    fac.Structure(f"{fname}.b", glist)
    fac.MemENTable(f"{fname}.b")
    fac.PrintTable(f"{fname}.b", f"{fname}", 1)
