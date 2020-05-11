import hackrf_cfile
import rtlsdr_cfile
import cosine_cfile
#import cosine_wave_zmq_pub
#import hackrf_zmq_pub
#import rtlsdr_zmq_pub
import sys
import time

# take the command line arguments
sdr_name = sys.argv[1]
center_freq = int(sys.argv[2])
sampling_rate = int(sys.argv[3])

# take the correct grc python file
if sdr_name == "hackrf":
    #grc = hackrf_zmq_pub.top_block()
    grc = hackrf_cfile.top_block()
elif sdr_name == "rtlsdr":
    grc = rtlsdr_cfile.top_block()
elif sdr_name == "cosine":
    grc = cosine_cfile.top_block()
else:
    grc = cosine_cfile.top_block()

# setting the center frequency
grc.set_center_freq(center_freq)

# setting the sampling rate
grc.set_samp_rate(sampling_rate)

# start the script
grc.start()

# running forever (until getting killed)
while True:
    pass