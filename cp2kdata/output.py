import sys

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from .block_parser.dft_plus_u import parse_dft_plus_u_occ
from .block_parser.forces import parse_atomic_forces_list
from .block_parser.geo_opt import parse_geo_opt
from .block_parser.header_info import parse_dft, parse_global, parse_header
from .block_parser.hirshfeld import parse_hirshfeld_pop_list
from .block_parser.mulliken import parse_mulliken_pop_list
from .block_parser.energies import parse_energies_list
from .block_parser.coordinates import parse_init_atomic_coordinates
from .block_parser.atomic_kind import parse_atomic_kinds


def check_run_type(run_type):
    implemented_run_type_parsers = ["ENERGY_FORCE", "ENERGY", "MD", "GEO_OPT"]
    if run_type in implemented_run_type_parsers:
        pass
    else:
        raise ValueError


class Cp2kOutput:
    """Class for parsing cp2k output"""

    def __init__(self, output_file) -> None:
        with open(output_file, 'r') as fp:
            self.output_file = "".join(fp.readlines())

        self.header_info = parse_header(self.output_file)
        self.global_info = parse_global(self.output_file)
        self.dft_info = parse_dft(self.output_file)
        try:
            check_run_type(self.global_info["run_type"])
        except ValueError:
            print(
                (
                    "Parser for Run Type {0} Haven't Been Implemented Yet!".format(
                        self.global_info["run_type"])
                )
            )
            sys.exit()
        if self.global_info["run_type"] == "GEO_OPT":
            # parse global info
            self.geo_opt_info = parse_geo_opt(self.output_file)
        else:
            self.geo_opt_info = None

        self.energies_list = parse_energies_list(self.output_file)
        self.init_atomic_coordinates, self.atom_kind_list, self.chemical_symbols = parse_init_atomic_coordinates(
            self.output_file)
        self.atomic_kind = parse_atomic_kinds(self.output_file)
        self.atomic_forces_list = parse_atomic_forces_list(self.output_file)
        self.mulliken_pop_list = parse_mulliken_pop_list(
            self.output_file, self.dft_info)
        self.hirshfeld_pop_list = parse_hirshfeld_pop_list(self.output_file)
        self.dft_plus_u_occ = parse_dft_plus_u_occ(self.output_file)

    def get_version_string(self) -> float:
        return self.header_info["version_string"]

    def get_run_type(self) -> float:
        return self.global_info["run_type"]

    def get_energies_list(self):
        return self.energies_list

    def get_atomic_kind(self):
        return self.atomic_kind

    def get_atom_kinds_list(self):
        return self.atom_kind_list

    def get_chemical_symbols(self):
        return self.chemical_symbols

    def get_chemical_symbols_fake(self):
        return self.atomic_kind[self.atom_kind_list-1]

    def get_init_atomic_coordinates(self):
        return self.init_atomic_coordinates

    def get_atomic_forces_list(self):
        return self.atomic_forces_list

    def get_mulliken_pop_list(self):
        return self.mulliken_pop_list

    def get_hirshfeld_pop_list(self):
        return self.hirshfeld_pop_list

    def get_dft_plus_u_occ(self):
        return self.dft_plus_u_occ

    def get_geo_opt_info(self):
        return self.geo_opt_info

    def get_geo_opt_info_plot(self):
        plt.rcParams.update(
            {
                'font.size': 20,
                'axes.linewidth': 2,
                'lines.marker': 'o',
                'lines.markeredgecolor': 'black',
                'lines.markeredgewidth': '0.5',
                'lines.markersize': 13,
                'xtick.major.size': 5,
                'xtick.major.width': 2,
                'ytick.major.width': 2
            }
        )
        geo_opt_steps = [one_geo_opt_info["step"]
                         for one_geo_opt_info in self.get_geo_opt_info()[1:]]
        max_step_size = [one_geo_opt_info["max_step_size"]
                         for one_geo_opt_info in self.get_geo_opt_info()[1:]]
        rms_step_size = [one_geo_opt_info["rms_step_size"]
                         for one_geo_opt_info in self.get_geo_opt_info()[1:]]
        max_grad = [one_geo_opt_info["max_gradient"]
                    for one_geo_opt_info in self.get_geo_opt_info()[1:]]
        rms_grad = [one_geo_opt_info["rms_gradient"]
                    for one_geo_opt_info in self.get_geo_opt_info()[1:]]

        fig = plt.figure(figsize=(24, 16), dpi=300)

        gs = GridSpec(2, 2, figure=fig)
        color = 'black'
        ax_max_step = fig.add_subplot(gs[0])
        ax_max_step.plot(geo_opt_steps, max_step_size,
                         color=color, markerfacecolor="#F2F2F2")
        ax_max_step.set_ylabel("Max Step Size")
        ax_max_step.set_xlabel("Optimzation Steps")
        ax_rms_step = fig.add_subplot(gs[1])
        ax_rms_step.plot(geo_opt_steps, rms_step_size,
                         color=color, markerfacecolor="#C6E070")
        ax_rms_step.set_ylabel("RMS Step Size")
        ax_rms_step.set_xlabel("Optimzation Steps")
        ax_max_grad = fig.add_subplot(gs[2])
        ax_max_grad.plot(geo_opt_steps, max_grad, color=color,
                         markerfacecolor="#91C46C")
        ax_max_grad.set_xlabel("Optimzation Steps")
        ax_max_grad.set_ylabel("Max Gradient")
        ax_rms_grad = fig.add_subplot(gs[3])
        ax_rms_grad.plot(geo_opt_steps, rms_grad, color=color,
                         markerfacecolor="#5C832F")
        ax_rms_grad.set_ylabel("RMS Gradient")
        ax_rms_grad.set_xlabel("Optimzation Steps")
        fig.suptitle("Geometry Optimization Information", fontsize=30)
        fig.tight_layout()
        fig.savefig("geo_opt_info.png")

    def to_ase_atoms(self):
        print("haven't implemented yet")
        pass
