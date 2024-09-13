import os

from . import compute


DEFAULT_ELEM = "Ar"
DEFAULT_CI_LEVEL = 0


def print_config(e_config):
    print("\t[")
    for line in e_config:
        print(f"\t{line},")
    print("\t]")


def read_default_econfig(n_elec):
    with open(f"ions/ion{n_elec}.dat") as f:
        elec_config = [line.rstrip("\n") for line in f]
    return elec_config


def facof() -> None:
    """FACOF - FAC On terminal Framework"""
    os.system("clear")
    while True:
        print("FACOF - FAC On terminal Framework")

        elem = input(f"\n Atom symbol (default {DEFAULT_ELEM}): ")
        if not elem:
            elem = DEFAULT_ELEM

        ci_level = input(
            f"\n Configuration interaction level (default {DEFAULT_CI_LEVEL}): "
        )

        if not ci_level:
            ci_level = DEFAULT_CI_LEVEL
        try:
            ci_level = int(ci_level)
        except:
            print("CI must be an integer. Exiting.")
            break

        energy_scheme_n = input("\n Flag for CA models ([1] for RDCA or [2] for FS): ")

        if energy_scheme_n == "1":
            energy_scheme = "RDCA"
        elif energy_scheme_n == "2":
            energy_scheme = "FS"
        else:
            print("Flag is not valid. Exiting.")
            break

        e_config = []
        print("\n Electronic configuration")
        use_ion = input("\tUse default ion configurations (y/n): ")

        if use_ion == "y":
            n_elec = int(
                input("\tSelec the number of electrons in the configuration: ")
            )
            e_config = read_default_econfig(n_elec)

        else:
            print("\tAdd new custom electron configuration:")
            print("\t[")
            while True:
                new_e_config = input("\t")
                if not new_e_config:
                    print("\t]")
                    break
                e_config.append(new_e_config)

        if not e_config:
            print("Electron configuration not provided. Exiting.")
            break

        compute.compute_lev(e_config, elem, energy_scheme, ci_level, include_tr=True)
        print("\n\tEnergy level generated! Exiting FACOF.")
        break


if __name__ == "__main__":
    facof()
