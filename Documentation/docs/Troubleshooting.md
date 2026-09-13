# Issues and Troubleshooting

This page lists problems that can come up when running the EKMC program, and what to do about them.

## ``ModuleNotFoundError: No module named 'SUMELF'``

EKMC depends on the ``SUMELF`` program. Install it into the same python environment:

```bash
pip3 install --upgrade --user git+https://github.com/geoffreyweal/SUMELF.git
```

See [Installation](Installation.md) for more information.

If SUMELF *is* installed and you still see this, check that you are not running from the folder that holds your repository clones — see [the section below](#importerror-or-modulenotfounderror-when-working-in-the-folder-that-holds-your-clones).

## ``ekmc: command not found``

The ``ekmc`` command is installed alongside the python package. If your terminal cannot find it, the most likely cause is that the ``bin`` folder of the python environment you installed EKMC into is not on your ``PATH``, or you installed EKMC into a different environment from the one you are using now.

Check which python you are using and that EKMC is installed into it:

```bash
which python3
pip3 show EKMC
```

## The kMC simulations will not run

EKMC performs its kinetic Monte Carlo steps in C, which must be compiled before the first run. If your simulations fail immediately, compile the C code:

```bash
ekmc compile
```

## My simulations have not finished

Use ``ekmc did_complete`` to see which simulations have completed and which have not:

```bash
ekmc did_complete
```

If jobs are being killed by slurm, they are likely running out of wall time or memory. Raise ``time`` and ``mem`` in the ``mass_submission_information`` dictionary in your setup script, then set up and resubmit those simulations.

## Setting up a crystal is very slow

Building the neighbourhood of every molecule in the crystal is the slow part of the setup. Raise ``no_of_cpus_for_setup`` when you call ``EKMC_Setup`` to use more cpus:

```python
EKMC_Setup(EKMC_settings, mass_submission_information, no_of_cpus_for_setup=8)
```

## ``ImportError: cannot import name 'EKMC_Multi_Setup'``

``EKMC_Multi_Setup`` no longer exists. Use ``EKMC_Setup``, which sets up one crystal at a time. To set up several crystals, loop over your settings:

```python
from EKMC import EKMC_Setup

for EKMC_settings, mass_submission_information in zip(all_EKMC_settings, all_mass_submission_information):
	EKMC_Setup(EKMC_settings, mass_submission_information)
```


## ``ImportError`` or ``ModuleNotFoundError`` when working in the folder that holds your clones

If you keep your clones of these programs together in one folder, like this:

~~~
Solar_Cell_Project/
|-- ACSD/
|-- ECCP/
|-- SUMELF/
|-- ...
~~~

then running a command or a python script **from that folder** fails with an error such as:

~~~
ImportError: cannot import name '__version__' from 'EKMC' (unknown location)
~~~

or:

~~~
ModuleNotFoundError: No module named 'SUMELF'
~~~

even though you installed everything correctly.

This happens because python searches the current directory first. The ``EKMC`` folder sitting there is the **git repository**, not the python package: the package is one level further in, at ``EKMC/EKMC``. The repository folder has no ``__init__.py``, so python treats it as an empty namespace package, finds no code inside it, and stops looking. Your installed copy is never reached.

The fix is to work from anywhere other than that folder. Change into the directory holding the crystals you are working on and run from there, which is what you would normally be doing anyway:

~~~bash
cd /path/to/my_crystals
ekmc --help
~~~

!!! tip

	Only the folder that *directly* contains the repository folders is affected. Subfolders of it are fine, and so is any unrelated directory.

## Something else has gone wrong

If you have found a problem that is not covered here, please [open an issue on GitHub](https://github.com/geoffreyweal/EKMC/issues) describing:

* what you were trying to do,
* the settings you used,
* and the full error message you received.
