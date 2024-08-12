# Полезные комманды FFMPEG

### Вывести размер картинки из видео
`ffprobe -v error -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=1 -i <file>`