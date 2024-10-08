# NexusDownloadFlow (NDF)

**NexusDownloadFlow (NDF)**
is an automated downloader designed to simplify the process of downloading mod lists from
[Nexus Mods](https://www.nexusmods.com/).
By automatically handling the download process,
it saves time and effort for users who frequently manage large collections of mods.

If NDF has been helpful for you when downloading mod lists, consider giving the repository 
a star :star: on GitHub to show your support!

## How Does It Work?

NexusDownloadFlow operates using computer vision principles, leveraging the power of OpenCV
and a template matching algorithm. This approach allows NDF to visually identify and interact
with the necessary buttons on the Nexus Mods website, such as:

- The `Slow download` button
- The `Click here` button

By automatically detecting these buttons, NDF simulates user clicks, allowing the mods to 
be downloaded without any manual intervention. This process enables seamless automation of
the mod downloading workflow, ensuring reliability and efficiency.

## Install

Download the latest version [here](https://github.com/greg-ynx/NexusDownloadFlow/releases).
NDF is only available for Windows as an executable.
If you wish to use it on another OS then download the project and run it with Python.

## Usage

### Basic Usage

While running `Wabbajack` modlist installer (for example), run `NexusDownloadFlow.exe`.

NDF should click on the `Slow download` button, automating the download process.

### Command-Line Interface (CLI) Usage

NexusDownloadFlow is a CLI application with commands that will allow you to configure and run the auto-downloader.

To access detailed information about the available commands and options in NDF, you can use the `--help` option.
This will display a list of all commands and their descriptions.

Example:

```bash
.\NexusDownloadFlow.exe --help
```

#### Run

You can run NDF simply by clicking on the executable or with the command line:

```bash
.\NexusDownloadFlow.exe
```

NDF offers three different launch modes to suit your specific needs when downloading mod lists.

Each mode determines how the templates are handled during the download process.

1. **Classic Mode (default)**
   <br>
   This is the default mode.
   It uses the predefined templates provided by NDF to automate the download of mods.
   No additional setup is required.
   To run in Classic mode, use:

```bash
.\NexusDownloadFlow.exe
```

2. **Custom Mode**
   <br>
   In Custom mode, NDF only uses the templates that you have manually added.
   This allows NDF to be fully adapted to your environment.
   To launch in Custom mode:

```bash
.\NexusDownloadFlow.exe --mode custom # Or .\NexusDownloadFlow.exe -m custom
```

3. **Hybrid Mode**
   <br>
   Hybrid mode combines both the default templates provided by NDF and your custom templates.
   This allows for a more comprehensive approach, using both standard automation and user-specific customizations.
   To launch in Hybrid mode:

```bash
.\NexusDownloadFlow.exe --mode hybrid # Or .\NexusDownloadFlow.exe -m hybrid
```

#### Adding Custom Templates

Users can enhance the flexibility of NDF by adding their own custom templates.
You can add your own templates using the `add-templates` command:

```bash
.\NexusDownloadFlow.exe add-templates path/of/custom_template.png path/of/second_custom_template.png
```

Custom templates are stored in a directory (`custom_templates`) located where `NexusDownloadFlow.exe` is.

#### Removing Custom Templates

In addition to adding templates,
NDF allows users to remove one or more custom templates that they have previously added.
This can be done using the `remove-templates` command.

**Removing a Specific Template**
To remove a specific custom template, use the following command:

```bash
.\NexusDownloadFlow.exe remove-templates custom_templates/custom_template_to_delete.png
```

**Removing All Custom Templates**
If you want to remove all custom templates at once, you can use the `--all` option with the `remove-templates` command:

```bash
.\NexusDownloadFlow.exe remove-templates --all
```

## Feature

### Run Command

The run feature is the core of NexusDownloadFlow (NDF),
allowing users to launch the automation process for downloading mods from Nexus Mods.
With this feature, users can choose between three distinct launch modes depending on their needs and preferences.

Available Modes:

1. Classic Mode (default)
   Runs the automation using the default templates provided by NDF.

2. Custom Mode
   Uses only the custom templates added by the user.

3. Hybrid Mode
   Combines both default and custom templates.

You can control NexusDownloadFlow (NDF) during the download process with keyboard shortcuts:
press F3 to `pause` or `resume` the download, and F4 to `stop` NDF at any time.

### Version Command

The `version` command allows users to quickly check which version of NexusDownloadFlow they are using.
This can be useful for troubleshooting or ensuring that you have the latest features and updates.

To display the current version, run:

```bash
.\NexusDownloadFlow version # Or -v
```

This will output the version number of NDF installed on your system.

### Add-Templates Command

The `add-templates` command allows you to add your custom templates to NexusDownloadFlow.

### Remove-Templates Command

The `remove-templates` command allows you to delete your custom templates from NexusDownloadFlow.

### Clear-Logs Command

The `clear-logs` command is used to delete all log files generated by NDF.
This helps to free up disk space and remove old log data that is no longer needed.

To clear the logs, use:

```bash
.\NexusDownloadFlow clear-logs
```

### Writing issue template for GitHub

The `issue` command helps users quickly create a pre-filled GitHub issue form for reporting bugs or requesting features
related to NexusDownloadFlow.

To generate the issue form, use:

```bash
.\NexusDownloadFlow issue
```

## Development requirements

Python v3.11 and:

```text
keyboard~=0.13.5
opencv-python~=4.10.0.84
mss~=9.0.2
PyAutoGUI~=0.9.54
psutil~=6.0.0
typer~=0.12.5
```
