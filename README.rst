Human Benchmark
===============

|badge_python_version|

.. |badge_python_version| image:: https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white
   :target: https://www.python.org
   :alt: Python version

*Since the dawn of time, humans have sought to prove their intellectual
prowess, outshining one another in feats of memory, reaction, and 
problem-solving. The `Human Benchmark <https://humanbenchmark.com/>`_
stands as a modern battleground for these cerebral showdowns. But 
the age of unchallenged human dominance is over. Machines have emerged, 
relentless and tireless, as rivals in the race for intellectual 
supremacy. This repository is dedicated to crafting methods that 
shatter records, obliterate benchmarks, and showcase the undeniable 
superiority of computers. Let the showdown begin.*

Table of Contents
-----------------

.. contents:: Table of Contents
   :local:
   :depth: 1

Benchmarks
----------

.. list-table::
   :header-rows: 1

   * - Benchmark
     - Description
     - Score
     - Percentile

   * - Reaction Time
     - Click as quickly as possible once the screen turns green
     - 78 ms
     - 99.9

More benchmarks will be added in the future!

Installation
------------

Use the following command to install this package: 

.. code-block:: bash

   pip install git+https://github.com/LouisCarpentier42/HumanBenchmark

This package has been developed using Python 3.11. Other Python versions
may work as well, but this has not been tested. 

Usage
-----

To start the script, simply run the following code: 

.. code-block:: python

   import human_benchmark
   human_benchmark.run()

A default configuration is provided, but it is also possible to pass the
path of a custom configuration file.

Once the script is running, open the benchmark you wish to solve. If the
benchmark is open, press the start key (defined by the configuration file)
to start solving the benchmark.

.. note::
   Once the script is running, control over the mouse and keyboard will be
   taken over. To stop the script, you can either press the stop key (defined
   in the configuration file), or you can move the mouse to the corner of
   the screen to trigger the fail-safe check.

Configuration file
------------------

The solvers can be customized via a configuration file in toml format. The
default configuration file can be found `here <https://github.com/LouisCarpentier42/HumanBenchmark/blob/main/human_benchmark/assets/config.toml>`_.
The config file must contain multiple sections: one for the general configuration
and one for the parameters of each benchmark. Below we describe the parameters.
The examples show the default configuration file

.. warning::
   The configuration file must define all parameters, there are no default values.

General
~~~~~~~
The configuration-parameters which are independent of the benchmark.

- ``start_key``: the key to press once the benchmark is open on the screen.
- ``stop_key``: the key to press to stop the process.
- ``delay``: the amount of delay after executing a construction with ``pyautogui``.

.. literalinclude:: human_benchmark/assets/config.toml
   :language: toml
   :start-after: [general]
   :end-before: [reaction_time]

Reaction Time
~~~~~~~~~~~~~

- ``nb_clicks``: the number of times that the solver should try to click to screen as quickly as possible.
- ``click_pause``: the time (in seconds) to pause after clicking the screen.
- ``auto_continue``: whether the solver should automatically continue after clicking or not.
- ``screenshot_width``: the width of the screenshot to take, which is used to check when to click.
- ``screenshot_height``: the height of the screenshot to take, which is used to check when to click.

.. literalinclude:: human_benchmark/assets/config.toml
   :language: toml
   :start-after: [reaction_time]

Credits
-------

This project is inspired by the `Human Benchmark Series <https://www.youtube.com/@codebulletsdayoff582>`_
of `Code Bullet <https://www.youtube.com/@CodeBullet>`_.
