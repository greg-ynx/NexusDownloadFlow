# Feature

## Run Command

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

## Version Command

The `version` command allows users to quickly check which version of NexusDownloadFlow they are using.
This can be useful for troubleshooting or ensuring that you have the latest features and updates.

To display the current version, run:

```bash
.\NexusDownloadFlow version # Or -v
```

This will output the version number of NDF installed on your system.

## Add-Templates Command

The `add-templates` command allows you to add your custom templates to NexusDownloadFlow.

## Remove-Templates Command

The `remove-templates` command allows you to delete your custom templates from NexusDownloadFlow.

## Clear-Logs Command

The `clear-logs` command is used to delete all log files generated by NDF.
This helps to free up disk space and remove old log data that is no longer needed.

To clear the logs, use:

```bash
.\NexusDownloadFlow clear-logs
```

## Writing issue template for GitHub

The `issue` command helps users quickly create a pre-filled GitHub issue form for reporting bugs or requesting features
related to NexusDownloadFlow.

To generate the issue form, use:

```bash
.\NexusDownloadFlow issue
```