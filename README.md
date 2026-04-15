# -File-Organizer
[ System: Auto-Organizer ]
Overview:
An event-driven, cross-platform file organization daemon. Built in Python, it monitors directories in real-time and automatically routes files (Images, Videos, Code, Executables) to the native system libraries based on their extensions.

Technical Advantage (Why it's superior):
Fully optimized. Instead of running aggressive folder-checking loops that waste processing power, the tool directly listens to OS kernel hooks. CPU cost while idle is zero, keeping RAM consumption nailed around 10MB. Perfect for rigs focused on maximum performance (FPS).

Core Features:

Immediate Monitoring: Reacts to on_created (downloaded files) and on_moved (dragged files) events in the exact same millisecond.

Smart Notification Bypass (Windows): Systems optimized with Regedits or anti-lag scripts usually have their alert panels stripped. This script bypasses Microsoft's native API and injects a custom, minimalist Toast directly on the screen, ensuring the alert never fails.

Linux Integration: Native support for distros, invoking lightweight alerts straight through the terminal's notify-send.

Download Safe: Filters in-transit files (.crdownload, .part, .tmp). The script is smart enough to wait for the download to finish before attempting to move it, preventing file corruption.

Anti-Overwrite System: Intelligent data loss protection. If the destination already has a file with the exact same name, it generates automatic versioning (_1, _2) instead of deleting the old one.
