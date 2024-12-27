# Human Benchmark

[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

*Since the dawn of time, humans have sought to prove their intellectual
prowess, outshining one another in feats of memory, reaction, and 
problem-solving. The [Human Benchmark](https://humanbenchmark.com/)
stands as a modern battleground for these cerebral showdowns. But 
the age of unchallenged human dominance is over. Machines have emerged, 
relentless and tireless, as rivals in the race for intellectual 
supremacy. This repository is dedicated to crafting methods that 
shatter records, obliterate benchmarks, and showcase the undeniable 
superiority of computers. Let the showdown begin.*

## Table of Contents
1. [Benchmarks](#benchmarks): An overview of the different benchmarks and the performance of the solvers.
2. [Installation](#installation): How to install the code. 
3. [Usage](#usage): How to use the code.
4. [Configuration file](#configuration-file): How to format the configuration file.
5. [Credits](#credits)

## Benchmarks

| Benchmark     | Description                                                              | Score    | Percntile |
|---------------|--------------------------------------------------------------------------|----------|-----------|
| Reaction Time | Click as quickly as possible once the screen turns green                 | 78 ms    | 99.9      |
| Target Aimer  | Targets pop up, which must be clicked as quickly as possible             | 50 ms    | 100.0     |
| Typing        | Type a given text as quickly as possible                                 | 5500 WPM | 100.0     |
| Verbal Memory | Remember a sequence of words and indicate if a new word already occurred | 1000     | 100.0     |

More benchmarks will be added in the future!

## Installation

Use the following command to install this package:
```bash
pip install git+https://github.com/LouisCarpentier42/HumanBenchmark
```
This project has been developed using Python 3.11. Other Python versions
may work as well, but this has not been tested. 

## Usage

To start the script, simply run the following code:
```python
import human_benchmark
human_benchmark.run()
```
A default configuration is provided, but it is also possible to pass the
path of a custom configuration file.

Once the script is running, open the benchmark you wish to solve. If the
benchmark is open, press the start key (defined by the configuration file)
to start solving the benchmark.

> :bulb: **Warning** :bulb: 
> 
> Once the script is running, control over the mouse and keyboard will be
> taken over. To stop the script, you can either press the stop key (defined
> in the configuration file), or you can move the mouse to the corner of
> the screen to trigger the fail-safe check.

## Configuration file

The solvers can be customized via a configuration file in toml format. The
default configuration file can be found [here](human_benchmark/assets/config.toml).
The config file must contain multiple sections: one for the general configuration
and one for the parameters of each benchmark. Below we describe the parameters.
The examples show the default configuration file.

> :warning: **Warning** :warning: 
>
> The configuration file must define all parameters, there are no default values.

If you only wish to adjust certain parameters from the default config, 
then you can call below code to create a copy of the default configuration
file as follwos:
```python
import human_benchmark
human_benchmark.save_default_config('new-config.toml')
```
This file can be adjusted as desired, after which you can pass 
the path of this new configuration file to the ``human_benchmark.run()``
method:
```python
import human_benchmark
human_benchmark.run(custom_config_path='new-config.toml')
```

### General

The configuration-parameters which are independent of the benchmark.

- ``start_key``: the key to press once the benchmark is open on the screen.
- ``stop_key``: the key to press to stop the process.
- ``delay``: the amount of delay after executing a construction with ``pyautogui``.
- ``exit_after_benchmark``: Whether to program should close after solving a benchmark or not.  

> :bulb: **Warning** :bulb: 
>
> If ``exit_after_benchmark = false``, then the program will continue looping. Before 
> starting to solve a benchmark (after the ``start_key`` has been pressed), the config
> file is reread. This means you can adjust the configuration file without having to 
> restart the program. 

```toml
[general]
start_key = 'esc'
stop_key = 'q'
delay = 0.0001
exit_after_benchmark = false
```

### Reaction Time

- ``nb_clicks``: the number of times that the solver should try to click to screen as quickly as possible.
- ``click_pause``: the time (in seconds) to pause after clicking the screen.
- ``auto_continue``: whether the solver should automatically continue after clicking or not.
- ``screenshot_width``: the width of the screenshot to take, which is used to check when to click.
- ``screenshot_height``: the height of the screenshot to take, which is used to check when to click.

```toml
[reaction_time]
nb_clicks = 5
click_pause = 1
auto_continue = true
screenshot_width = 3
screenshot_height = 3
```

### Target Aimer

- ``nb_targets``: the number of targets to click. 
- ``target_size``: the number of pixels that must have the target color before the solver considers that the target is shown.
- ``quantile``: indicates which pixel with the target color to click (to avoid clicking other pixels with the same color).
- ``click_pause``: the time (in seconds) to pause after clicking the screen. 

```toml
[target_aimer]
nb_targets = 30
target_size = 50
quantile = 0.5
click_pause = 0.015
```

### Typing

> :warning: **Warning** :warning: 
>
> For this benchmark, you should also install the [tesseract software](https://github.com/UB-Mannheim/tesseract/wiki). 
> This benchmark has only been tested on Windows, and might not work on
> mac or linux. 

- ``delay_start``: time delay (in seconds) before starting to type. 
- ``delay_key_press``: time delay (in seconds) between each key press.
- ``text_height``: the height of the text box in pixels. 
- ``path_to_tesseract``: the path to the tesseract.exe file. 

```toml
[typing]
delay_start = 1.5
delay_key_press = 0
text_height = 225
path_to_tesseract = "C:/Program Files/Tesseract-OCR/tesseract.exe"
```

### Verbal Memory

> :warning: **Warning** :warning: 
>
> For this benchmark, you should also install the [tesseract software](https://github.com/UB-Mannheim/tesseract/wiki). 
> This benchmark has only been tested on Windows, and might not work on
> mac or linux. 

- ``delay_start``: the time (in seconds) before starting the solver.
- ``delay_click``: the time (in seconds) to wait after clicking a button. 
- ``screenshot_x``: the relative center of the word (in x-direction) compared to the start screen.
- ``screenshot_y``: the relative center of the word (in y-direction) compared to the start screen.
- ``screenshot_width``: the width of the screenshot containing the word. 
- ``screenshot_height``: the height of the screenshot containing the word. 
- ``confidence``: The confidence criteria for locating the different buttons.
- ``max_score``: The maximum score, after which the script should stop. If set to ``-1``, there is no limit. 
- ``path_to_tesseract``: the path to the tesseract.exe file. 

```toml
delay_start = 0.1
delay_click = 0.025
screenshot_x = 0.5
screenshot_y = 0.48
screenshot_width = 700
screenshot_height = 100
confidence = 0.9
max_score = 1000
path_to_tesseract = "C:/Program Files/Tesseract-OCR/tesseract.exe"
```

## Credits

This project is inspired by the [Human Benchmark Series](https://www.youtube.com/@codebulletsdayoff582)
of [Code Bullet](https://www.youtube.com/@CodeBullet).
