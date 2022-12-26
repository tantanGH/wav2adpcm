#
#  wav2adpcm.py - wave file to X680x0 ADPCM data converter in Python (using soundfile library)
#  https://github.com/tantanGH/wav2adpcm/
#
#  implemented based on the below Dialogic ADPCM format specifications:
#  https://en.wikipedia.org/wiki/Dialogic_ADPCM
#

import argparse
import soundfile as sf
import numpy as np

from scipy.signal import butter, lfilter

step_adjust = [ -1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8 ]

step_size = [  16,  17,  19,  21,  23,  25,  28,  31,  34,  37,  41,  45,   50,   55,   60,   66,
               73,  80,  88,  97, 107, 118, 130, 143, 157, 173, 190, 209,  230,  253,  279,  307,
              337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411, 1552 ]

def decode_adpcm(code,step_index,last_data):

    ss = step_size[ step_index ]

    delta = ( ss >> 3 )

    if ( code & 0x01 ):
        delta += ( ss >> 2 )

    if ( code & 0x02 ):
        delta += ( ss >> 1 )

    if ( code & 0x04 ):
        delta += ss

    if ( code & 0x08 ):
        delta = -delta
    
    estimate = last_data + delta

    if (estimate > 2047):
        estimate = 2047

    if (estimate < -2048):
        estimate = -2048

    step_index += step_adjust[ code ]

    if (step_index < 0):
        step_index = 0

    if (step_index > 48):
        step_index = 48

    return (estimate,step_index)

def encode_adpcm(current_data, last_estimate, step_index):

    ss = step_size[ step_index ]

    delta = current_data - last_estimate

    code = 0x00
    if ( delta < 0 ):
        code = 0x08         # bit3 = 1
        delta = -delta

    if ( delta >= ss ):
        code += 0x04        # bit2 = 1
        delta -= ss

    if ( delta >= (ss>>1) ):
        code += 0x02        # bit1 = 1
        delta -= ss>>1

    if ( delta >= (ss>>2) ):
        code += 0x01        # bit0 = 1
    
    # need to use decoder to estimate
    (estimate,adjusted_index) = decode_adpcm(code,step_index,last_estimate)

    return (code,estimate,adjusted_index)

def lowpass_filter(data, cutoff, fs, order):
    b, a = butter(order, cutoff / (0.5 * fs), btype='lowpass')
    y = lfilter(b, a, data)
    return y

def convert_wave_to_adpcm( wave_file, adpcm_file, filter_flag, volume_db ):

    # open the input WAVE file
    original_data, sample_rate = sf.read( wave_file )

    # apply the low-pass filter at 18kHz to the original data
    filtered_data = lowpass_filter( original_data, cutoff=18000, fs=sample_rate, order=5 ) if ( filter_flag != 0 ) else original_data

    # convert the stereo data to mono by averaging the left and right channels
    mono_data = np.mean( original_data, axis=1 )

    # convert the desired volume in dB to a scaling factor
    scaling_factor = 10 ** ( volume_db / 20 )

    # adjust the volume of the audio data by multiplying by the scaling factor
    adjusted_data = mono_data * scaling_factor

    # resampling to 15625Hz
    resampled_data = sf.resample( adjusted_data, sample_rate, 15625 )

    print(resampled_data[0:100])

    last_estimate = 0
    step_index = 0
    adpcm_data = []

    for i,x in enumerate( resampled_data ):

        ( code, estimate, adjusted_index ) = encode_adpcm( x//16, last_estimate, step_index )

        if ( i % 2 == 0 ):
            adpcm_data.append( code )
        else:
            adpcm_data[-1] |= code << 4

        last_estimate = estimate
        step_index = adjusted_index

    with open( adpcm_file, 'wb' ) as af:
        af.write( bytes( adpcm_data ))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("infile",help="input WAVE file")
    parser.add_argument("outfile",help="output ADPCM file")
    parser.add_argument("-f","--filter",help="apply low-pass filter (1:yes(default),0:no)",type=int,default=1,choices=[0,1])
    parser.add_argument("-v","--volume",help="adjust volume in dB [-20 to 20]",type=int,default=0)

    args = parser.parse_args()

    # execute conversion in script mode
    convert_wave_to_adpcm(args.infile,args.outfile,args.filter,args.volume)
