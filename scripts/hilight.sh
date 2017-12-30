#!/bin/bash
# usage: ./highlight.sh orig.jpg semseg.png color_people.jpg

pid=$$
convert $1 -colorspace Gray /tmp/hilight-${pid}-gray.jpg
convert $2 -fill white -opaque 'rgb(220,20,60)' -fill black +opaque white /tmp/hilight-${pid}-mask.png
convert -composite /tmp/hilight-${pid}-gray.jpg $1 /tmp/hilight-${pid}-mask.png $3
rm /tmp/hilight-${pid}-*.jpg
