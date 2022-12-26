#
#  wav2adpcm_pydub.py - wave file to X680x0 ADPCM data converter in Python (using pydub library)
#  https://github.com/tantanGH/wav2adpcm/
#
#  implemented based on the below Dialogic ADPCM format specifications:
#  https://en.wikipedia.org/wiki/Dialogic_ADPCM
#

import argparse

from pydub import AudioSegment

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

def convert_wave_to_adpcm( wave_file, adpcm_file, filter_flag, volume_adjust ):

    # Open the audio file
    audio = AudioSegment.from_file( wave_file, format='wav', warn=False )

    # Adjust the volume (default zero adust)
    adjusted_audio = audio + volume_adjust

    # Apply a low-pass filter at 18kHz (option, but default)
    filtered_audio = adjusted_audio.low_pass_filter( 18000 ) if filter_flag != 0 else adjusted_audio

    # to mono
    mono_audio = filtered_audio.set_channels( 1 )

    # to 15.6kHz
    rated_audio = mono_audio.set_frame_rate( 15625 )

    # source data samples (still 16bit)
    signed_16bit_samples = rated_audio.get_array_of_samples()

    last_estimate = 0
    step_index = 0
    adpcm_data = []

    for i,x in enumerate( signed_16bit_samples ):

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
