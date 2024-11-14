# aeon_feeder

this repo is under development

1. Register Mapping

   | Name        | MessageType | Address | PayloadType | Range      | Access | Default Value | Description                                    |
   | ----------- | ----------- | ------- | ----------- | ---------- | ------ | ------------- | ---------------------------------------------- |
   | `PEL_SND`   | `Write`     | `36`    | `U16`       | `[0, 255]` | `WR`   | `0`           | Deliver 1 pellet when write opration triggered |
   | `BBK_DET`   | `Event`     | `32`    | `U8`        | `[0, 255]` | `R`    | `0`           | Send the value 1 when the pellet delivered     |
   | `DUMMY`     | `Write`     | `35`    | `U16`       | `[0]`      | `WR`   | `0`           | Empty Register for backward compatibility      |
   | `WHEEL_ANG` | `Event`     | `90`    | `U16`       | `[0, 359]` | `R`    | `0`           | Return the current position of the wheel       |
