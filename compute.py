import re
import os

from pfac import fac


def default_file_name(elem, energy_scheme, ci_level) -> str:
    """Return default name for an energy level file."""
    if ci_level == -1:
        return f"{elem}_{energy_scheme}_NOCI"
    return f"{elem}_{energy_scheme}_{ci_level}"


def remove_b(path):
    """Remove binary files (.b) in path"""
    for file in os.listdir(path):
        if not re.search(".b", file):
            continue
        os.remove(f"{path}/{file}")


def compute_lev(
    path: str,
    e_config: list[str],
    elem: str = "K",
    energy_scheme: str = "RDCA",
    ci_level: int = 0,
    include_tr: bool = False,
) -> None:
    """Compute energy levels for a given element and electron configuration."""
    fac.Reinit(0)

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

    fname = default_file_name(elem, energy_scheme, ci_level)
    fpath = os.path.relpath(f"{path}/{fname}", os.getcwd())

    fac.Structure(fpath + ".lev.b", glist)
    fac.MemENTable(fpath + ".lev.b")
    fac.PrintTable(fpath + ".lev.b", fpath + ".lev", 1)

    if include_tr:
        fac.TransitionTable(fpath + ".tr.b", glist, glist)
        fac.PrintTable(fpath + ".tr.b", fpath + ".tr")
