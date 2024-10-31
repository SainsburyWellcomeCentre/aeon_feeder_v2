# aeon_feeder

this repo is under development

1. Register Mapping

   | Name        | MessageType | Address | PayloadType | Range         | Access | Default Value | Description                                      |
   | ----------- | ----------- | ------- | ----------- | ------------- | ------ | ------------- | ------------------------------------------------ |
   | `PEL_SND`   | `Write`     | `33`    | `U8`        | `[1, 255]`    | `W`    | `Null`        | Deliver a certain number of pellets to the wheel |
   | `BBK_DET`   | `Event`     | `37`    | `U8`        | `[0, 1]`      | `R`    | `0`           | Send the value 1 when the pellet delivered       |
   | `WHEEL_ANG` | `Event`     | `90`    | `Float`     | `[0, 359.99]` | `R`    | `0`           | Return the current position of the wheel         |
