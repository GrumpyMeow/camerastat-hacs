# Camera Statistic
A HACS custom Home Assistant integration to get statistic from a camera image.
It uses the [ImageStat](https://pillow.readthedocs.io/en/stable/reference/ImageStat.html) operation from Pillow.

I created this integration as i wanted to have automation switch from day <-> night mode. I was unable to get my camera to do this itself in a desired way.

This integration should also make it possible to check if your red ferrari is parked on your drive way.

The default update interval is 10 minutes (600 seconds). 

Current issues:
* Initially the sensors will have no value, but they should be populated at the first update
* The entity names have an incorrect name like: "camera_statistic_for_none_camera_statistic_for_none_b_mean". This is caused that the selected camera entity does not have a name defined. You can do this via the Home Assistant gui.
* An icon would be nice

Tips/notes:
* If your camera provides a substream, use that one. This should reduce the resource utilitzation.
* The fastest update-interval is 5seconds. This to not introduce stability issues.
* Be aware that storing all sensor-values will significantly increase the size of your Home Assistant database. You should disable sensors which you are not interested in.
