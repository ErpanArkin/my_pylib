#!/usr/bin/python3

from pymatgen.io.vasp.outputs import Outcar, Locpot, Poscar
from pymatgen.util.plotting import pretty_plot
import numpy as np
import sys


'''
This script plot the LOCPOT files along the direction
specified by the 1st argument: 0 = a direction; 1 = b direction; ...
This requires CONTCAR OUTACR LOCPOT vasprun.xml files.
It is generalized version of WorkFunctionAnalyzer from pymatgen
for handling all directions.
'''


class WorkFunctionAnalyzer(object):
    """
    A class that post processes a task document of a vasp calculation (from
        using drone.assimilate). Can calculate work function from the vasp
        calculations and plot the potential along the c axis. This class
        assumes that LVTOT=True (i.e. the LOCPOT file was generated) for a
        slab calculation and it was insert into the task document along with
        the other outputs.

    .. attribute:: efermi

        The Fermi energy

    .. attribute:: locpot_along_c

        Local potential in eV along points along the  axis

    .. attribute:: vacuum_locpot

        The maximum local potential along the c direction for
            the slab model, ie the potential at the vacuum

    .. attribute:: work_function

        The minimum energy needed to move an electron from the
            surface to infinity. Defined as the difference between
            the potential at the vacuum and the Fermi energy.

    .. attribute:: slab

        The slab structure model

    .. attribute:: along_c

        Points along the c direction with same
            increments as the locpot in the c axis

    .. attribute:: ave_locpot

        Mean of the minimum and maximmum (vacuum) locpot along c

    .. attribute:: sorted_sites

        List of sites from the slab sorted along the c direction

    .. attribute:: ave_bulk_p

        The average locpot of the slab region along the c direction
    """

    def __init__(self, structure, locpot_along_c, efermi, shift=0):
        """
        Initializes the WorkFunctionAnalyzer class.

        Args:
            structure (Structure): Structure object modelling the surface
            locpot_along_c (list): Local potential along the c direction
            outcar (MSONable): Outcar vasp output object
            shift (float): Parameter to translate the slab (and
                therefore the vacuum) of the slab structure, thereby
                translating the plot along the x axis.
        """
        # set direction
        self.direction = int(sys.argv[1])

        # properties that can be shifted
        slab = structure.copy()
        if self.direction == 0:
            slab.translate_sites(
                [i for i, site in enumerate(slab)], [shift, 0, 0])
        elif self.direction == 1:
            slab.translate_sites(
                [i for i, site in enumerate(slab)], [0, shift, 0])
        elif self.direction == 2:
            slab.translate_sites(
                [i for i, site in enumerate(slab)], [0, 0, shift])
        self.slab = slab
        self.sorted_sites = sorted(
            self.slab, key=lambda site: site.frac_coords[self.direction])

        # Get the plot points between 0 and c
        # increments of the number of locpot points
        locpot_along_c = locpot_along_c
        self.along_c = np.linspace(0, 1, num=len(locpot_along_c))
        locpot_along_c_mid, locpot_end, locpot_start = [], [], []
        for i, s in enumerate(self.along_c):
            j = s + shift
            if j > 1:
                locpot_start.append(locpot_along_c[i])
            elif j < 0:
                locpot_end.append(locpot_along_c[i])
            else:
                locpot_along_c_mid.append(locpot_along_c[i])
        self.locpot_along_c = locpot_start + locpot_along_c_mid + locpot_end

        # get the average of the signal in the bulk-like region of the
        # slab, i.e. the average of the oscillating region. This gives
        # a rough appr. of the potential in the interior of the slab
        bulk_p = [p for i, p in enumerate(self.locpot_along_c) if
                  self.sorted_sites[-1].frac_coords[self.direction] > self.along_c[i]
                  > self.sorted_sites[0].frac_coords[self.direction]]
        self.ave_bulk_p = np.mean(bulk_p)

        # shift independent quantities
        self.efermi = efermi
        self.vacuum_locpot = max(self.locpot_along_c)
        # get the work function
        self.work_function = self.vacuum_locpot - self.efermi
        # for setting ylim and annotating
        self.ave_locpot = (self.vacuum_locpot - min(self.locpot_along_c)) / 2

    def get_locpot_along_slab_plot(self, label_energies=True,
                                   plt=None, label_fontsize=10):
        """
        Returns a plot of the local potential (eV) vs the
            position along the c axis of the slab model (Ang)

        Args:
            label_energies (bool): Whether to label relevant energy
                quantities such as the work function, Fermi energy,
                vacuum locpot, bulk-like locpot
            plt (plt): Matplotlib pylab object
            label_fontsize (float): Fontsize of labels

        Returns plt of the locpot vs c axis
        """

        plt = pretty_plot(width=10, height=8) if not plt else plt

        # plot the raw locpot signal along c
        plt.plot(self.along_c, self.locpot_along_c, 'b--')

        # Get the local averaged signal of the locpot along c
        xg, yg = [], []
        for i, p in enumerate(self.locpot_along_c):
            # average signal is just the bulk-like potential when in the slab region
            if p < self.ave_bulk_p \
                or self.sorted_sites[-1].frac_coords[self.direction] >= self.along_c[i] \
                    >= self.sorted_sites[0].frac_coords[self.direction]:
                yg.append(self.ave_bulk_p)
                xg.append(self.along_c[i])
            else:
                yg.append(p)
                xg.append(self.along_c[i])
        xg, yg = zip(*sorted(zip(xg, yg)))
        plt.plot(xg, yg, 'r', linewidth=2.5, zorder=-1)

        # make it look nice
        if label_energies:
            plt = self.get_labels(plt, label_fontsize=label_fontsize)
        plt.xlim([0, 1])
        plt.ylim([min(self.locpot_along_c),
                  self.vacuum_locpot + self.ave_locpot * 0.2])
        if self.direction == 0:
            plt.xlabel(r"Fractional coordinates ($\hat{a}$)", fontsize=25)
        elif self.direction == 1:
            plt.xlabel(r"Fractional coordinates ($\hat{b}$)", fontsize=25)
        elif self.direction == 2:
            plt.xlabel(r"Fractional coordinates ($\hat{c}$)", fontsize=25)
        plt.xticks(fontsize=15, rotation=45)
        plt.ylabel(r"Potential (eV)", fontsize=25)
        plt.yticks(fontsize=15)

        return plt

    def get_labels(self, plt, label_fontsize=10):
        """
        Handles the optional labelling of the plot with relevant quantities
        Args:
            plt (plt): Plot of the locpot vs c axis
            label_fontsize (float): Fontsize of labels
        Returns Labelled plt
        """

        maxc = self.sorted_sites[-1].frac_coords[self.direction]
        minc = self.sorted_sites[0].frac_coords[self.direction]
        # determine whether most of the vacuum is to
        # the left or right for labelling purposes
        vleft = [i for i in self.along_c if i <= minc]
        vright = [i for i in self.along_c if i >= maxc]
        if max(vleft) - min(vleft) > max(vright) - min(vright):
            label_in_vac = (max(vleft) - min(vleft)) / 2
        else:
            label_in_vac = (max(vright) - min(vright)) / 2 + maxc

        # label the vacuum locpot
        label_in_bulk = maxc - (maxc - minc) / 2
        plt.plot([0, 1], [self.vacuum_locpot] *
                 2, 'b--', zorder=-5, linewidth=1)
        xy = [label_in_bulk, self.vacuum_locpot + self.ave_locpot * 0.05]
        plt.annotate(r"$V_{vac}=%.2f$" % (self.vacuum_locpot), xy=xy,
                     xytext=xy, color='b', fontsize=label_fontsize)

        # label the fermi energy
        plt.plot([0, 1], [self.efermi] * 2, 'g--',
                 zorder=-5, linewidth=3)
        xy = [label_in_bulk, self.efermi + self.ave_locpot * 0.05]
        plt.annotate(r"$E_F=%.2f$" % (self.efermi), xytext=xy,
                     xy=xy, fontsize=label_fontsize, color='g')

        # label the bulk-like locpot
        plt.plot([0, 1], [self.ave_bulk_p] * 2, 'r--', linewidth=1., zorder=-1)
        xy = [label_in_vac, self.ave_bulk_p + self.ave_locpot * 0.05]
        plt.annotate(r"$V^{interior}_{slab}=%.2f$" % (self.ave_bulk_p),
                     xy=xy, xytext=xy, color='r', fontsize=label_fontsize)

        # label the work function as a barrier
        plt.plot([label_in_vac] * 2, [self.efermi, self.vacuum_locpot],
                 'k--', zorder=-5, linewidth=2)
        xy = [label_in_vac, self.efermi + self.ave_locpot * 0.05]
        plt.annotate(r"$\Phi=%.2f$" % (self.work_function),
                     xy=xy, xytext=xy, fontsize=label_fontsize)

        return plt

    def is_converged(self, min_points_frac=0.015, tol=0.0025):
        """
        A well converged work function should have a flat electrostatic
            potential within some distance (min_point) about where the peak
            electrostatic potential is found along the c direction of the
            slab. This is dependent on the size of the slab.
        Args:
            min_point (fractional coordinates): The number of data points
                +/- the point of where the electrostatic potential is at
                its peak along the c direction.
            tol (float): If the electrostatic potential stays the same
                within this tolerance, within the min_points, it is converged.

        Returns a bool (whether or not the work function is converged)
        """

        conv_within = tol * (max(self.locpot_along_c) -
                             min(self.locpot_along_c))
        min_points = int(min_points_frac * len(self.locpot_along_c))
        peak_i = self.locpot_along_c.index(self.vacuum_locpot)
        all_flat = []
        for i in range(len(self.along_c)):
            if peak_i - min_points < i < peak_i + min_points:
                if abs(self.vacuum_locpot - self.locpot_along_c[i]) > conv_within:
                    all_flat.append(False)
                else:
                    all_flat.append(True)
        return all(all_flat)

    @staticmethod
    def from_files(poscar_filename, locpot_filename, outcar_filename, shift=0):
        p = Poscar.from_file(poscar_filename)
        l = Locpot.from_file(locpot_filename)
        o = Outcar(outcar_filename)
        return WorkFunctionAnalyzer(p.structure,
                                    l.get_average_along_axis(int(sys.argv[1])),
                                    o.efermi, shift=shift)


if len(sys.argv) != 2:
    raise ValueError('Please provide the direction as the 1st argument.')

wf = WorkFunctionAnalyzer.from_files('CONTCAR', 'LOCPOT', 'OUTCAR')
wf_plot = wf.get_locpot_along_slab_plot()
wf_plot.tight_layout()
wf_plot.savefig('vasp_locpot.png')
wf_plot.show()
