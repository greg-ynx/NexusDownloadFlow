# NexusDownloadFlow 2022 : Auto clicker script using computer vision

NexusDownloaderFlow (NDF) 2022 is a script that take screenshots and classify if any template match with the current
screenshot taken. It was made in order to automate process with `Wabbajack modlist installation of Nexus' mods` in which
you have to manually click on `Slow download` button is your NexusMods account is not premium.

## How to use NDF 2022 ?

Just execute `NexusDownloadFlow 2022.exe` and open your NexusMods' download page.

## Auto clicker is not clicking

Do not worry, you have to replace the templates files where you installed NDF with the one you will screenshot:
`NexusDownloadFlow 2022/assets/template{x}.png`

+ `template1.png` is the raw `Slow download` button
+ `template2.png` is the `Slow download` button with mouse over
+ `template3.png` is the `Click here` link appearing five seconds after clicking on `Slow download` button

## Credits

Thanks to @parsiad for inspiring me with his repository named `parsiad/nexus-autodl` 
(I could not download his auto clicker).

Requirements used for this script are :
+ PyAutoGUI~=0.9.53
+ opencv-python==4.5.5.64
+ mss~=6.1.0