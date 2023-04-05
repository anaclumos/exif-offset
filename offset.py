from datetime import datetime
import os
import piexif
import pytz
import tqdm

timezone = "America/New_York"

tz = pytz.timezone(timezone)

camera_date = datetime(2019, 1, 1, 0, 1, 0)
actual_date = datetime(2023, 3, 13, 15, 6, 33).astimezone(tz)

# for file in target folder
# get file date
# get file exif date

target = "./target"
all_files = os.listdir(target)
for file in tqdm.tqdm(all_files):
    if (
        file.endswith(".JPG")
        or file.endswith(".jpg")
        or file.endswith(".jpeg")
        or file.endswith(".JPEG")
    ):
        exif_dict = piexif.load(os.path.join(target, file))
        print(file)
        print(
            "File date: ",
            datetime.fromtimestamp(os.path.getmtime(os.path.join(target, file))),
        )
        print("File exif date: ", exif_dict["0th"][piexif.ImageIFD.DateTime])
        print(
            "File exif date original: ",
            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal],
        )
        print(
            "File exif date digitized: ",
            exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized],
        )
        # the correct time = this_photo_date - camera_date + actual_date as New York time
        # b'2019:01:01 04:12:18'
        this_photo_date = datetime.strptime(
            exif_dict["0th"][piexif.ImageIFD.DateTime].decode("utf-8"),
            "%Y:%m:%d %H:%M:%S",
        )
        correct_time = (this_photo_date - camera_date + actual_date).astimezone(tz)
        print("Correct time: ", correct_time)
        # write correct time to exif
        new_date = correct_time.strftime("%Y:%m:%d %H:%M:%S")
        exif_dict["0th"][piexif.ImageIFD.DateTime] = new_date
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_date
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_date
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, os.path.join(target, file))
