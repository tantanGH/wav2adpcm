# wav2adpcm
Wave format PCM data to X68000 ADPCM data converter in Python

### Install

    pip install git+https://github.com/tantanGH/wav2adpcm.git

### Usage

    wav2adpcm [options] <input-wave-file> <output-adpcm-file>

Note that you need to add wav2adpcm installed folder to your PATH environment variable.

To surpress warnings messages in case you don't have ffmpeg, you just ignore it or modify wav2adpcm execution script in ~/Library/Python/3.x/bin/ like below.

    #!/Library/Developer/CommandLineTools/usr/bin/python3 -W ignore

This is macOS case. Change install path to your environment accordingly.
