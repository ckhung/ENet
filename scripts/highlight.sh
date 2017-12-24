#!/bin/bash
# usage: ./highlight.sh orig.jpg result.jpg color_people.jpg

pid=$$
convert $1 -colorspace Gray /tmp/hilight-${pid}-gray.jpg
convert $2 -fuzz 3% -fill white -opaque 'rgb(220,20,60)' -fill black +opaque white /tmp/hilight-${pid}-mask.jpg
convert -composite /tmp/hilight-${pid}-gray.jpg $1 /tmp/hilight-${pid}-mask.jpg $3
rm /tmp/hilight-${pid}-*.jpg
