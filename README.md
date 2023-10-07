# NexusDownloadFlow: Auto-downloader for Nexus Mods

NexusDownloadFlow (NDF) is a program that automates the download process with `Wabbajack modlist installation of Nexus
Mods` in which you have to manually click on `Slow download` button if your Nexus Mods account is not premium.

## How to use NexusDownloadFlow?

### Without Wabbajack
Execute `NexusDownloadFlow.exe` and open your Nexus Mods download page.

### With Wabbajack
Execute `NexusDownloadFlow.exe` while the mod list is downloading.

## Auto-clicker is not clicking

Do not worry, you have to replace the template files where you installed NDF with the one you will screenshot:
`NexusDownloadFlow 2022/assets/template{x}.png`

+ `template1.png` is the raw `Slow download` button
+ `template2.png` is the `Slow download` button with mouse over
+ `template3.png` is the `Click here` link appearing five seconds after clicking on `Slow download` button

If your issue persists, maximize the Nexus Mods page.

## Your issue still persist?

Open an issue here, and if possible, give the scenario in which you had this issue, which version of NDF you are using
and provide a screenshot of your logs or the contents of your current `nexus-download-flow-logs.log` file.

## Credits

Thanks to [parsiad](https://github.com/parsiad) for inspiring me with his repository named 
[`parsiad/nexus-autodl`](https://github.com/parsiad/nexus-autodl).
