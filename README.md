# HeartRateStreamer

An Apple Watch app that streams your real-time heart rate data to another device (e.g., PC) via the local network.

|![app_idle](./imgs/app_idle.png)|![app_active](./imgs/app_active.png)|
| --- | --- |

## Quick Start

This repository contains a WatchOS app `HeartRateStreamer` for transmitting real-time heart rate data and a simple receiver `HeartRateReceiver` for testing. You can try this app by following these steps:

1. **Deploy the App**: Open `HeartRateStreamer/HeartRateStreamer.xcodeproj` with XCode, compile the WatchOS app, and deploy it to your Apple Watch.
2. **Deploy the Receiver**: On the receiving device (such as a PC), use Python to run the example receiver `HeartRateReceiver/main.py`. This program will start an HTTP server on port `8000` to receive heart rate data.
   - here is an example of the terminal output
   - ```
     INFO:root:Starting HTTP server...
     INFO:root:IP addresses: ['fe80::ce12:f9fa:b9a8:afc8', 'fe80::b078:4987:7979:86b9', '10.1.0.3', '192.168.3.2', '172.29.0.1']
     INFO:root:Server port: 8000
     ```
3. **Check your Network**: Ensure that your **Apple Watch**, the **receiving device**, and the **iPhone paired with the Apple Watch** are on the same network.
3. **Start Transmission**: Launch the app on your Apple Watch, enter the address and port number of the receiving service in the input field (e.g. `192.168.3.2:8000`), and click the green button below to start transmitting heart rate data. You need to allow this app to access your health data and heart rate data when launching it for the first time.
4. **View the Data**: Once data transmission starts, the terminal of the receiving service will output the received heart rate data.
   - here is an example of the terminal output
   - ```
     192.168.3.71 - - [15/Oct/2024 20:52:46] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'timestamp': 1729021969.4095302, 'heartRate': 60}
     192.168.3.71 - - [15/Oct/2024 20:52:57] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'heartRate': 57, 'timestamp': 1729021981.00441}
     192.168.3.71 - - [15/Oct/2024 20:53:03] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'heartRate': 61.99999999999999, 'timestamp': 1729021986.300029}
     192.168.3.71 - - [15/Oct/2024 20:53:07] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'timestamp': 1729021990.7547832, 'heartRate': 61}
     192.168.3.71 - - [15/Oct/2024 20:53:11] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'heartRate': 60, 'timestamp': 1729021995.1046262}
     192.168.3.71 - - [15/Oct/2024 20:53:22] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'heartRate': 56, 'timestamp': 1729022005.405021}
     192.168.3.71 - - [15/Oct/2024 20:53:25] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'heartRate': 64, 'timestamp': 1729022008.652159}
     192.168.3.71 - - [15/Oct/2024 20:53:27] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'timestamp': 1729022010.8522391, 'heartRate': 60}
     192.168.3.71 - - [15/Oct/2024 20:53:34] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'timestamp': 1729022017.80251, 'heartRate': 61}
     192.168.3.71 - - [15/Oct/2024 20:53:41] "POST /heart-rate-endpoint HTTP/1.1" 200 -
     INFO:root:{'timestamp': 1729022024.609463, 'heartRate': 60}
     ```
5. (Optional) **For VRChat users**, you can install the Python module `python-osc`. When running the receiver example, it will send the heart rate data to the VRChat client via OSC protocol, the value of beat per minute will be set to the HR parameter of the avatar (See: [OSC Overview for VRChat](https://docs.vrchat.com/docs/osc-overview)).


## FAQ

### Why I need my iPhone connected to the same network?

When the iPhone is available, the Apple Watch will prioritize routing any network data through the iPhone, and the data will be sent via the iPhone. When the iPhone is unavailable, it will use its own WiFi connection to send network data. (See: [Apple Documentation](https://developer.apple.com/documentation/watchos-apps/keeping-your-watchos-app-s-content-up-to-date#Test-your-update-code-with-different-configurations))
