BEGIN{b=0}
//{if(NF==1&&$0!~" ")b=0;if($0==key)b=1}
/^    /{if(b==1&&(pattern==""||$0~pattern)){gsub(/^[ ]+/,"",$0);print $0}}
