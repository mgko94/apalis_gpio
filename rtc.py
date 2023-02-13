#!/usr/bin/env python

import fcntl, struct, glob

RTC_RD_TIME=0x80247009

# Identify RTCs
rtcList = glob.glob('/dev/rtc[0-9]')
print "RTCs: ", rtcList, "\n"

# Read each RTC
for rtc in rtcList
    #  struct rtc_time {
    #    int tm_sec;
    #    int tm_min;
    #    int tm_hour;
    #    int tm_mday;
    #    int tm_mon;
    #    int tm_year;
    #    int tm_wday;
    #    int tm_yday;
    #     int tm_isdst;
    #  };
    a=struct.pack('iiiiiiiii', 0,0,0,0,0,0,0,0,0)

    fo=open(rtc)

    input=fcntl.ioctl(fo.fileno(), RTC_RD_TIME, a)
    result=struct.unpack('iiiiiiiii', input)

    print rtc + ": " + str(1900+result[5]) + "-" + str(1+result[4]) + "-" + str(result[3]) + " " + \
          str(result[2]) + ":" + str(result[1]) + ":" + str(result[0]) + " UTC"
