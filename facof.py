import os
import compute_lev


DEFAULT_ELEM = 'K'
DEFAULT_CI_LEVEL = 0
DEFAULT_E_CONFIG = ['1*2 2*5',
                    '1*2 2*4 3*1',
                    '1*2 2*4 4*1',
                    '1*2 2*4 5*1',
                    '1*2 2*3 3*2']


def print_config(e_config):
    print('\t[')
    for line in e_config:
        print(f'\t{line},')
    print('\t]')


def facof() -> None:
    """FACOF - FAC On terminal Framework
    """
    os.system('clear')
    while True:
        print('FACOF - FAC On terminal Framework')

        elem = input(f'\n Atom symbol (default {DEFAULT_ELEM}): ')
        if not elem:
            elem = DEFAULT_ELEM

        ci_level = input(f'\n Configuration interaction level (default {DEFAULT_CI_LEVEL}):')
        if ci_level.isdigit():
            ci_level = int(ci_level)
        elif not ci_level:
            ci_level = DEFAULT_CI_LEVEL
        else:
            print('CI must be an integer. Exiting.')
            break

        print('\n Flag for CA models:')
        print('\t[1] RDCA')
        print('\t[2] FS')
        energy_scheme_n = input('\t')
        if energy_scheme_n == '1':
            energy_scheme = 'RDCA'
        elif energy_scheme_n == '2':
            energy_scheme = 'FS'
        else:
            print('Flag is not valid. Exiting.')
            break

        e_config = []
        print('\n Electronic configuration')
        print('\n\tDefault electronic configuration: ')
        print_config(DEFAULT_E_CONFIG)
        print('\n\tAdd new allowed electron configurations (if none use default):')
        print('\t[')
        while True:
            new_e_config = input('\t')
            if not new_e_config:
                print('\t]')
                break
            e_config.append(new_e_config)
        if not e_config:
            e_config = DEFAULT_E_CONFIG

        compute_lev.compute_lev(e_config, energy_scheme, ci_level, elem=elem)
        print('\n\tEnergy level generated! Exiting FACOF.')
        break


if __name__ == '__main__':
    facof()
