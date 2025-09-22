# Полезные комманды FFMPEG

### Вывести размер картинки из видео
`ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=1 -i <file>`

### Обрезка файла по времени
`ffmpeg -ss 01:15:00 -t 00:15:00 -i <file> -vcodec copy -acodec copy <file>`

`ffmpeg -ss 01:15:00 -to 01:30:00 -i <file> -vcodec copy -acodec copy <file>`

`-ss 01:19:00 ` - время начала

`-t 00:05:00` - длительность обрезки

### Обрезка картинки видео
`ffmpeg -i <file> -vf "scale=1280:720" -acodec copy <file>`