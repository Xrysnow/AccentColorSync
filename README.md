# AccentColorSync

This project can change accent color of win10 and sync with WallpaperEngine.

### Usage

Add WebSocket to your webpage-based wallpaper:

```js
let socketURL = "ws://localhost:55001"
let socket = new WebSocket(socketURL);
let socketReopen = function() {
	socket.close();
   	socket = new WebSocket(socketURL);
	socket.onclose = socketReopen;
};
socket.onclose = socketReopen;
// invoke this when you set a new image
let sendCurrent = function(path)
{
	if (socket.readyState == WebSocket.OPEN) {
		try {
			socket.send(decodeURI(path));
		} catch (e) {
			socketReopen();
		}
	}
};
```
This can be used with wallpapers such as [Personal Slideshow](https://steamcommunity.com/sharedfiles/filedetails/?id=796697921). But you can also send other messages to satisfy your demand.

Then run the server:

```bash
python main.py
```

### Requirements

- Python 3
- Windows 10 (test on 21H2)
