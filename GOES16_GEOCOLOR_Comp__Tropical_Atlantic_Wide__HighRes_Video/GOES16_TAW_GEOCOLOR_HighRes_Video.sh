#!/bin/bash

img_dir="./images"
python_file=$(realpath $(ls | grep 'py'))

if [ ! -d $img_dir ]; then
    mkdir -p $img_dir
    cd $img_dir
    echo -e "\n Downloading image files..."
    python $python_file
    echo -e "\n Downloads DONE"
elif [ -d $img_dir ]; then
    cd $img_dir
    echo -e "\n Downloading image files..."
    python $python_file
    echo -e "\n Downloads DONE"
fi

if [[ $(ls . | grep .jpg) == *.jpg ]]; then
    num_jpg=$(ls ./*.jpg | wc -l)
    echo -e "\n Downloaded $num_jpg jpg files."
fi

dir=$(dirname $PWD)

v_date="$(date +%Y)y$(date +%j)d$(date +%V)w__$(date +%b)_$(date +%d)__$(date +%H)h$(date +%M)m$(date +%S)s_$(date +%Z)"
v_name="${v_date}__GOES16-ABI-taw-GEOCOLOR"

### H264_NVENC
echo -e "\n Rendering h.264 video."
f_name="${v_name}__h264_nvenc.mp4"
ffmpeg -hwaccel cuda -pattern_type glob -i "*_GOES16-ABI-taw-GEOCOLOR-7200x4320.jpg" -vf scale=4096:-1 -c:v h264_nvenc -preset p7 -tune lossless -level 6.2 -rc vbr -pix_fmt yuv444p -r 30 $dir/${f_name} > /dev/null
if [ -f $f_name ]; then
    echo -e "\n File saved as:\n  $f_name in $dir"
fi
    
### HEVC_NVENC
echo -e "\n Rendering HEVC video."
f_name="${v_name}__hevc_nvenc.hevc"
ffmpeg -hwaccel cuda -pattern_type glob -i "*_GOES16-ABI-taw-GEOCOLOR-7200x4320.jpg" -c:v hevc_nvenc -preset p7 -tune lossless -level 6.2 -rc vbr -pix_fmt yuv444p -r 30 $dir/${f_name} > /dev/null
if [ -f $f_name ]; then
    echo -e "\n File saved as:\n  $f_name in $dir"
fi
