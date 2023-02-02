*********************************************
Fitting 2-body repulsive potentials using CCS
*********************************************

When we use the Curvature Constrained Splines method (`CCS <https://pubs.acs.org/doi/10.1021/acs.jctc.0c01156>`_) to fit a repulsive potential, we fit a 2-body potential
to reproduce, as closely as possible, the energy difference between DFT reference
energies and the corresponding *electronic energies* from DFTB. 

This example revolves around some of the CCS scripts to handle the various tasks
involved in the fitting of a repulsive potential. The data used in this example 
originates from the paper `Towards an efficient f-in-core/f-in-valence switchable
description for DFTB calculations of Ce 4f states in ceria`.

Data for the f-in-core and f-in-valence approched are located in the folders ``IN_CORE`` and ``IN_VAL``, respectively.  

Two ASE data-bases, one containing the reference DFT data (computed with VASP) and
one containing the corresponding DFTB data are provided in the current example.  

.. tip:: 
   
 The script ``RUN`` can be used to automatically execute the various steps of this example. The scrips can be used as templates when using CCS to fit repulsive potentials for a new system.  


0. Install required software
============================
Before we start we need to install CCS. The code is available `here <https://github.com/Teoroo-CMC/CCS.git>`_ .
Make sure to add the CCS binary folder, ``CCS/bin/`` , to your path.

1. Collect the DFT en DFTB electroinc energies
==============================================
Using the script ``ccs_build_db`` from the CCS-package, we can build two ase data-bases  
containing the DFT and DFTB data. These data-bases are used in the next step. 
We need a list pointing to the DFT data and the corresponding DFTB data. 
The code assume that the we provide locations of the DFT data (e.g. ``OUTCAR.gz`` or any other ASE readable file containing a geometry and corresponding energy) in the 
first column and the DFTB data in the second column (should be a ``results.tag`` file). 


.. admonition:: Task
  :class: info

  *** (In this example, this step have allready been performed. The raw-data used is not provided.) ***

  In order create the data-bases we make a folder (``TRAINING_DATA`` in the current example)  with a file pointing to the training-data (``list``) and the
  execute the command:

  .. code-block::

    ccs_build_db --mode DFTB --file_list list --DFT_DB DFT.db --DFTB_DB DFTB.db

  Example of a ``list`` file::

    ../RAW_DATA/BULK_CeO2/5.20/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.20/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.21/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.21/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.22/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.22/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.23/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.23/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.24/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.24/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.25/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.25/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.26/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.26/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.27/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.27/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.28/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.28/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.29/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.29/DFTB/results.tag
    ../RAW_DATA/BULK_CeO2/5.30/VASP/OUTCAR    ../RAW_DATA/BULK_CeO2/5.30/DFTB/results.tag

.. tip::
  You can get a quick overview of the training-data using the Atomic Simulation 
  Environment (`ASE <https://wiki.fysik.dtu.dk/ase/>`_) by issuing the command: 

  .. code-block::
 
    ase-gui DFT.db 
   
  (see figure below)

  .. figure:: ase.png
      :alt: ase
      :width: 600
      :align: center

      With the Atomic Simulation Environment we can get an quick overview 
      of the training-data. We can, amongst much other, browse the structures 
      and plot the energies.    

.. caution::

  All pairs you intend to make a repulsive potential for must have a dummy spline at the 
  bottom of the it's skf-file when the DFTB data is generated.      

2. Produce the specific training-file for CCS
=============================================
We collect pair-wise distances from the structures stored in the two 
data-bases and create a file called ``structures.json`` that CCS 
use for the fitting.

.. admonition:: Task
  :class: info

  Go to the ``FITTING`` folder and execute:

  .. code-block::

    ccs_fetch --mode DFTB --DFT_DB TRAINING_DATA/DFT.db --DFTB_DB TRAINING_DATA/DFTB.db

.. caution::

  Never use a cut-off radius that is smaller than used in the fitting (see next step). The defualt in ccs_fetch is 6.0 Å.


3. Now we can do fitting! 
=========================
We provide the setting in a file ``CCS_input.json`` where we speicify the cut-off radius
the resolution of the spline and the type of constraints (rep = stricktly repulsive, 
sw=attractive at long distance and repulsive at short distance).

CCS_input.json::

    {
    "Twobody":{
    	"Ce-O":{
    		"Rcut":5.3,
    		"Resolution":0.13,
                    "Swtype":"rep",
                    "const_type":"Mono"
    	}
    },
    
    "Onebody":["Ce"],
    
    "Reference":"structures.json",
    
    "General":{
    	"interface":"DFTB",
            "merging":"True"
    }
    
    }


.. admonition:: Task
  :class: info

  Check or modify the file ``CCS_input.json`` and execute:

  .. code-block::

   ccs_fit 

.. caution::

  Rcut must be smaller than the cut-off radius in the previus step!   

4. Enjoy succes!(?)  
===================
The quallity of the fit is provided in ``CCS_error.out`` and the resulting
parameters in ``CCS_params.json``. 

.. tip::

  You can use the ``plot_fit.py`` script in the ``FITTING`` folder to
  get an overview of the fitting quallity.

  .. code-block::

     python plot_fit.py


  .. figure:: corrplot.png
      :alt: ase
      :width: 400
      :align: center

      Correlation plot showing the reuslts of the fitting. The target repulsive energies
      are given at the x-axis and the resulting repulisive from the fitting is shown at 
      the y-axis.    

5. Convert to DFTB+ Slater-Koster format
========================================
DFTB+ have a specific format for the 2-body potential, a cubic 
spline-table appended at the end of the Slater-Koster file. We need
to convert the ``CCS_params.json`` file to this format.

.. admonition:: Task
  :class: info

  Execute: 

  .. code-block::

     ccs_export_sktable CCS_params.json

  The result are printed to files ``X-Y.spl`` where ``X`` and ``Y`` are
  the corresponding elements in the 2-body potential, e.g  
  ``X=Ce, Y=O``.

.. tip::

  You can use the ``plot_rep.py`` script in the ``FITTING`` folder to
  display the resulting Ce-O spline repulsive contained in the file ``Ce-O.spl`` .

  .. code-block::

     python plot_rep.py
    
  .. figure:: Reps.png
      :alt: ase
      :width: 600
      :align: center

      Comparative plot showing a 2-body spline repulsive for Ce-O fitted to a data-set
      of 75 structures.

6. Use the new parameters
=========================
Replace the dummy-spline in the ``.skf`` file contained in the folder ``SKF-FILES/REFITTED`` with the data from the ``.spl`` file generated in step 5 and 
you are good to go.

In the folder ``VALIDATION`` you can perform a validation of the generated parameters. Two examples are provided: 

    *  Cell optimization of bulk ceria (located in the folder: ``VALIDATION/CELL_OPT``)
    *  Phonon spectra of of bulk ceria (located in the folder: ``VALIDATION/PHONONS``)

In order to run these examples you need `DFTB+ <https://dftbplus.org/>`_ and `phonopy <https://phonopy.github.io/phonopy/>`_.  



Cell optimization of bulk ceria
-------------------------------

.. admonition:: Task
  :class: info

  Go to the folder ``VALIDATION/CELL_OPT`` and run dftb by executing the command:

  .. code-block::

    dftb+

  The results can be inspected by comparing the files ``in.gen`` and ``Optimized.gen`` which contains the 
  optimized DFT geometry (the starting point of the DFTB optimization) and the DFTB optimized geometry, respectively. 

  Note: The ``dftb_in.hsd`` file point to the Slater-Koster files contained in the ``SKF-FILES/REFITTED`` folder.

 
Phonon spectra of bulk ceria
----------------------------


.. admonition:: Task
  :class: info

  Go to the folders ``VALIDATION/PHONONS/001`` and ``VALIDATION/PHONONS/001`` and
  perform a dftb+ calculation in each of them. To generate the phonon spectra we go
  to the folder ``VALIDATION/PHONONS`` and make use of ``phonopy`` by using the 
  following commands:  
 
  .. code-block::

     phonopy -f {001..002}/results.tag --dftb+
     phonopy -p band.conf -s --dftb      
 
  The reults can visualized using the ``plot_phonon_spectra.py`` script which produce a figure
  like the one shown below.

  .. figure:: phonons.png
      :alt: ase
      :width: 600
      :align: center

      Comparison of phonon spectra calculated with the parametrized DFTB+ method and VASP.   



 

