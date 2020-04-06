# shift the center of mass to zero
set sel [atomselect top all]
set n [molinfo top get numframes]
for { set i 0 } { $i < $n } { incr i } {  
  $sel frame $i
  $sel update
  set x [measure center $sel]
  set y [vecscale -1 $x]
  $sel moveby $y
}
