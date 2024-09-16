# Run module

Run command module.

## scripts.cli.run.run.cli_run

Run the auto-downloader.

* **Raises:**
  * **KeyboardInterrupt** – Raised when the user interrupts the program.
  * **FailSafeException** – Raised when the mouse position is on one of the corners of the screen.

Should not be raised (open an issue on GitHub if it happens).
:raises ValueError: Should not be raised (open an issue on GitHub if it happens).
:raises Exception: For currently unknown exceptions (open an issue on GitHub if it happens).

```python
def cli_run(mode: str) -> None:
    setup_logging()
    logging.info(__RUN_STARTING_MESSAGE)
    try:
        match mode:
            case RunModeEnum.CLASSIC:
                classic_run()
            case RunModeEnum.CUSTOM:
                custom_run()
            case RunModeEnum.HYBRID:
                hybrid_run()
            case _:
                hybrid_run()
    except KeyboardInterrupt:
        logging.info(__EXITING_INFO_MESSAGE)
    except FailSafeException:
        logging.error(__FAILSAFE_ERROR_MESSAGE)
    except ValueError as e:
        logging.error(e)
        logging_report()
    except Exception as e:
        logging.error(e)
        logging_report()
    finally:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
        else:
            logging.warning(__SCREENSHOT_DOES_NOT_EXIST_MESSAGE)
        logging.info(__PROGRAM_ENDED_MESSAGE)
        stop_logging()
        input("Press any key to exit...")
```

## scripts.cli.run.run.classic_run

Launch classic execution method using built-in templates.

```python
def classic_run() -> None:
    logging.info(__RUNNING_MESSAGE.format(mode=RunModeEnum.CLASSIC))
    launch_ndf(__DEFAULT_TEMPLATES)
```

## scripts.cli.run.run.custom_run

Launch custom execution method using user-provided templates.

```python
def custom_run() -> None:
    logging.info(__RUNNING_MESSAGE.format(mode=RunModeEnum.CUSTOM))
    custom_templates: list[MatLike] = __get_custom_templates()
    if custom_templates:
        launch_ndf(custom_templates)
        return
    logging.error(__CUSTOM_RUN_NO_CUSTOM_TEMPLATE_FOUND_ERROR_MESSAGE)
```

## scripts.cli.run.run.hybrid_run

Launch hybrid execution method using built-in and custom templates.

```python
def hybrid_run() -> None:
    logging.info(__RUNNING_MESSAGE.format(mode=RunModeEnum.HYBRID))
    hybrid_templates: list[MatLike] = __DEFAULT_TEMPLATES + __get_custom_templates()
    launch_ndf(hybrid_templates)
```

## scripts.cli.run.run.launch_ndf

Launch the auto-downloader.

```python
def launch_ndf(templates: list[MatLike]) -> None:
    global is_running, is_paused
    is_running = True

    __init_hotkeys()

    edged_templates: list[MatLike] = __get_edged_templates(templates)
    with mss() as mss_instance:
        while is_running:
            __when_paused()
            monitors_size: dict[str, int] = mss_instance.monitors[0]
            monitors_left_top: tuple[int, int] = __if_monitors_left_top_present(monitors_size)
            screenshot: MatLike = cv2.imread(next(mss_instance.save(mon=-1, output=SCREENSHOT_PATH)))
            grayscale_screenshot: MatLike = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            multiscale_match_template(edged_templates, grayscale_screenshot, monitors_left_top)
```

## scripts.cli.run.run.multiscale_match_template

Apply multiscale template matching algorithm.

* **Parameters:**
  * **templates** – List of edged templates to match.
  * **screenshot** – Screenshot where the search is running.
  * **left_top_coordinates** – Left-top pixel of the system monitor(s).

```python
def multiscale_match_template(templates: list[MatLike], screenshot: MatLike, left_top_coordinates: tuple[int, int]) -> None:
    for scale in __SCALES:
        resized_screenshot: MatLike = __resize_screenshot(screenshot, scale)
        edged_screenshot: MatLike = cv2.Canny(resized_screenshot, 50, 200)
        for template in templates:
            potential_match: tuple[float, Sequence[int]] = __get_potential_match(edged_screenshot, template)
            potential_match_value: float = potential_match[0]
            potential_match_location: Sequence[int] = potential_match[1]
            if __is_match_found(potential_match_value):
                logging.info("Match found!")
                match_location_x: int = potential_match_location[0]
                match_location_y: int = potential_match_location[1]
                match_left_top_location: tuple[int, int] = (
                    match_location_x + left_top_coordinates[0],
                    match_location_y + left_top_coordinates[1],
                )
                template_height: int = template.shape[0]
                template_width: int = template.shape[1]
                target: tuple[float, float] = (
                    match_left_top_location[0] + template_width / 2,
                    match_left_top_location[1] + template_height / 2,
                )
                __click_on_target(target)
                sleep(6)
                return
```

## scripts.cli.run.run.pause_resume

Pause or resume the auto download process.

```python
def pause_resume() -> None:
    global is_paused
    if is_paused:
        is_paused = False
        logging.info(__RESUME_NDF_MESSAGE)
    else:
        is_paused = True
        logging.info(__PAUSE_NDF_MESSAGE)
```

## scripts.cli.run.run.stop

Stop the auto download process.

```python
def stop() -> None:
    """Stop the auto download process."""
    global is_running, is_paused
    is_running = False
    is_paused = False
    logging.info(__STOPPING_NDF_MESSAGE)
```
