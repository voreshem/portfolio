!/bin/bash

img_dir="./images"
python_file=$(realpath $(ls | grep 'py'))

if [ ! -d $img_dir ]; then
    mkdir -p $img_dir
    cd $img_dir
    python $python_file
elif [ -d $img_dir ]; then
    cd $img_dir
    python $python_file    
fi

dir=$(dirname $PWD)

v_date="$(date +%Y)y$(date +%j)d$(date +%V)w__$(date +%b)_$(date +%d)__$(date +%H)h$(date +%M)m$(date +%S)s_$(date +%Z)"
v_name="${v_date}__GOES16-ABI-taw-GEOCOLOR"

### H264_NVENC
f_name="${v_name}__h264_nvenc.mp4"
ffmpeg -hwaccel cuda -pattern_type glob -i "*_GOES16-ABI-taw-GEOCOLOR-7200x4320.jpg" -vf scale=4096:-1 -c:v h264_nvenc -preset p7 -tune lossless -level 6.2 -rc vbr -pix_fmt yuv444p -r 30 ${f_name}

    
### HEVC_NVENC
f_name="${v_name}__hevc_nvenc.hevc"
ffmpeg -hwaccel cuda -pattern_type glob -i "*_GOES16-ABI-taw-GEOCOLOR-7200x4320.jpg" -c:v hevc_nvenc -preset p7 -tune lossless -level 6.2 -rc vbr -pix_fmt yuv444p -r 30 ${f_name}
