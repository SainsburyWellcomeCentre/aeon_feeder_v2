# aeon_feeder

this repo is under development

1. Register Mapping

   | Name          | MessageType | Address | PayloadType | Range          | Access | Default Value | Description                                                     |
   | ------------- | ----------- | ------- | ----------- | -------------- | ------ | ------------- | --------------------------------------------------------------- |
   | `PEL_SND`     | `Write`     | `33`    | `U8`        | `[1, 255]`     | `W`    | `Null`        | Deliver a certain number of pellets to the wheel                |
   | `PEL_COUNT`   | `Read`      | `34`    | `U16`       | `[0, 65535]`   | `R`    | `0`           | Returns the number of pellet has dropped since power-up         |
   | `BBK_VAL`     | `Read`      | `35`    | `U16`       | `[0, 65535]`   | `R`    | `0`           | Return the raw value of the beam break                          |
   | `BBK_THLD`    | `Write`     | `36`    | `U16`       | `[0, 65535]`   | `W/R`  | `8000`        | Set the threshold for beam break for pellet detection           |
   | `BBK_GAIN`    | `Write`     | `38`    | `FLOAT`     | `[1e-3, 1e+3]` | `W/R`  | `1`           | Set the sensitvity of the beam break                            |
   | `BBK_DET`     | `Event`     | `37`    | `U8`        | `[0, 1]`       | `R`    | `0`           | Send the value 1 when the pellet delivered                      |
   | `WHEEL_ANG`   | `Read`      | `40`    | `U16`       | `[0, 359]`     | `R`    | `0`           | Return the current position of the wheel                        |
   | `WHEEL_COUNT` | `Read`      | `39`    | `U32`       | [0, $2^{32}$]  | `R`    | `0`           | Returns the turns of wheel has rotated since power-up           |
   | `WHEEL_THLD`  | `Write`     | `41`    | `U32`       | [0, $2^{32}$]  | `W/R`  | `0`           | Set the threshold for wheel rotation to trigger pellet delivery |
   | `AUTO_EN`     | `Write`     | `42`    | `U8`        | `[0, 1]`       | `W/R`  | `0`           | Automatic operation of the feeder according to set thresholds   |

