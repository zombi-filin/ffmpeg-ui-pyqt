# Полезные комманды FFMPEG

### Вывести размер картинки из видео
`ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=1 -i <file>`

### Обрезка файла по времени
`ffmpeg -ss 01:19:00 -t 00:05:00 -i <file> -vcodec copy -acodec copy <file>`

`-ss 01:19:00 ` - время начала

`-t 00:05:00` - длительность обрезки