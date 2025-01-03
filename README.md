# SwitchBot QuietDrift  for Home Assistant

Until QuietDrift is implemented directly in Home Assistant (which might take a while), you can use
this custom component. It relies on implementation details a bit, but I think it is a reasonable
temporary solution.

## Setup

### Config file

Add the following line to configuration.yaml:

```
switchbot_quietdrift:
```

### GUI

Not yet supported.

## Usage:

Set position this way (you have to call an action, formerly known as a service):

```
action: switchbot_quietdrift.set_curtain_position
data:
  speed: 1
  position: 90
  entity_id: cover.<your_cover_entity>
```

There is also an older action `cover.switchbot_quietdrift_set_curtain_position`.
It does the very same job, but the old one cannot be easily configured via the GUI, only by using YAML.
