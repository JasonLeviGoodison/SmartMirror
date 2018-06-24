# SmartMirror
The intention of this application is to load it on a raspberry pi and put a display behind a mirror. 
The assistant will display/tell you about information like weather and calendar events.

This smart mirror has a virtual assistant, called Jarvis, and a GUI display. 
I will outline what functionality each of these 2 features have and then I'll talk about how to set 
this up on your own Raspberry pi.

### GUI Display:
In the top left, you'll see information about the weather, including temp, an image, weather summary.
The top right has time and date. The bottom of the window has upcoming events for the next week according to your
Google Calendar. This updates every 15 minutes. So if you add an event to your day tomorrow expect to see it on the mirror soon.

### Virtual Assistant: Jarvis
To talk to the assistant, say "Hey Jarvis". You'll hear a beep and then you can ask for your assistant to do something.
The virtual assistant has a lot of the same functionality that the GUI does. It can tell you the weather and what events
you have scheduled for today.

The main difference is that you can ask Jarvis to set calendar events for you. So if you ask Jarvis to add an event to your calendar
it will show up on the mirror in < 15 minutes. If you ask Jarvis for your events for the day, it will be up to date with the
new event you just added.

### Set up
 // TODO
