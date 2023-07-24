# Camera Statistic
A HACS custom Home Assistant integration to get statistic from a camera image.
It uses the [ImageStat](https://pillow.readthedocs.io/en/stable/reference/ImageStat.html) operation from Pillow.

I created this integration as i wanted to have automation switch from day <-> night mode. I was unable to get my camera to do this itself in a desired way.

This integration should also make it possible to check if your red ferrari is parked on your drive way.

The default update interval is 10 minutes (600 seconds). 

Screenshots:
![afbeelding](https://github.com/GrumpyMeow/camerastat-hacs/assets/12073499/8d508063-b698-48ec-bb7e-dc73617bcda8)
![afbeelding](https://github.com/GrumpyMeow/camerastat-hacs/assets/12073499/2b5d832a-c8b9-4a25-a3b5-9de077e589df)
![afbeelding](https://github.com/GrumpyMeow/camerastat-hacs/assets/12073499/0c54b7be-c88a-4bc8-83cd-64839ab9461b)


Current issues:
* Initially the sensors will have no value, but they should be populated at the first update
* The entity names have an incorrect name like: "camera_statistic_for_none_camera_statistic_for_none_b_mean". This is caused that the selected camera entity does not have a name defined. You can do this via the Home Assistant gui.
* An icon would be nice
* Conversion from 0-255 still needs to be converted to percentages (0-100)

Tips/notes:
* If your camera provides a substream, use that one. This should reduce the resource utilitzation.
* The fastest update-interval is 5seconds. This to not introduce stability issues.
* Be aware that storing all sensor-values will significantly increase the size of your Home Assistant database. You should disable sensors which you are not interested in.
* You can trigger an update via a service-call:
  ```
  service: homeassistant.update_entity
  data: {}
  target:
     entity_id: >-
       sensor.camera_statistic_for_voortuin_substream_camera_statistic_for_voortuin_substream_b_mean
  ```

