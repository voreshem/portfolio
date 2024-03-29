#!/bin/bash

clear

dir="${PWD}"

date="$(date +%Y)y$(date +%j)d$(date +%V)w__$(date +%b)_$(date +%d)__$(date +%H)h$(date +%M)m$(date +%S)s_$(date +%Z)"

name="${date}__GOES16-ABI-taw-GEOCOLOR"

img_dir="${dir}/${date}__images"

python_file="$(realpath $(ls | grep 'py'))"

if [ ! -d $img_dir ]; then
    mkdir -p $img_dir
    cd $img_dir
    echo -e "\n Downloading image files...\n"
    python $python_file
    clear
    echo -e "\n Downloads DONE"
elif [ -d $img_dir ]; then
    cd $img_dir
    echo -e "\n Downloading image files...\n"
    python $python_file
    clear
    echo -e "\n Downloads DONE"
fi

if [[ $(ls . | grep .jpg) == *.jpg ]]; then
    num_jpg="$(ls ./*.jpg | wc -l)"
    echo -e "\n Downloaded $num_jpg jpg files."
fi

### H264_NVENC
echo -e "\n RENDERING h.264 video..."
f_name="${name}__h264_nvenc.mp4"
f_path="$dir/${f_name}"
ffmpeg -hide_banner -loglevel quiet -hwaccel cuda -pattern_type glob -i "${img_dir}/*_GOES16-ABI-taw-GEOCOLOR-7200x4320.jpg" -vf scale=4096:-1 -c:v h264_nvenc -preset p7 -tune lossless -level 6.2 -rc vbr -pix_fmt yuv444p -r 30 ${f_path} 1> /dev/null
if [ -f $f_path ]; then
    echo -e "\n File SAVED as:\n  $f_name \n in:\n  $dir"
elif [ ! -f $f_path ]; then
    echo -e "\n Saving h.264 FAILED"
fi
    
### HEVC_NVENC
echo -e "\n RENDERING hevc video..."
f_name="${name}__hevc_nvenc.hevc"
f_path="$dir/${f_name}"
ffmpeg -hide_banner -loglevel quiet -hwaccel cuda -pattern_type glob -i "${img_dir}/*_GOES16-ABI-taw-GEOCOLOR-7200x4320.jpg" -c:v hevc_nvenc -preset p7 -tune lossless -level 6.2 -rc vbr -pix_fmt yuv444p -r 30 ${f_path} 1> /dev/null
if [ -f $f_path ]; then
    echo -e "\n File SAVED as:\n  $f_name \n in:\n  $dir"
elif [ ! -f $f_path ]; then
    echo -e "\n Saving hevc FAILED"
fi
