# aeon_feeder_v2

this repo is under development

1. Register Mapping

   | Name         | MessageType | Address | PayloadType | Range      | Access | length | Description                                              |
   | ------------ | ----------- | ------- | ----------- | ---------- | ------ | ------ | -------------------------------------------------------- |
   | `BBK_DET`    | `Event`     | `32`    | `U8`        | `255`      | `R`    | `1`    | Send the value 255 when the pellet delivered             |
   | `DUMMY`      | `Write`     | `35`    | `U16`       | `[0]`      | `WR`   | `1`    | Empty Register for backward compatibility                |
   | `PEL_SND`    | `Write`     | `36`    | `U16`       | `[0, 255]` | `WR`   | `1`    | Deliver 1 pellet when write opration triggered           |
   | `WHEEL_ENCO` | `Event`     | `90`    | `U16`       | `[0, 359]` | `R`    | `2`    | Return the current value of the wheel [Angle, Magnitude] |
