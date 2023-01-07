# wav2adpcm
Wave format PCM data to X68000 ADPCM data converter in Python

### Install

    pip install git+https://github.com/tantanGH/wav2adpcm.git

[Windowsユーザ向けPython導入ガイド](https://github.com/tantanGH/distribution/blob/main/windows_python_for_x68k.md)

### Usage

    wav2adpcm [options] <input-wave-file> <output-adpcm-file>

Output ADPCM format is 15.6kHz mono (fixed).

    options:
        -f[0 or 1] ... 1:apply low-pass filter (default:1)
        -v[dB]     ... volume adjust in dB (default:0)
        -t[sec]    ... trim at specific secoonds
        -e         ... fade out at the end
        -d         ... dump mode (C source code generation)
        -a         ... use assembler code for dump mode

Note that you need to add wav2adpcm installed folder to your PATH environment variable.

To suppress warnings messages in case you don't have ffmpeg, you just ignore it or modify wav2adpcm execution script in `~/Library/Python/3.x/bin/` like below.

    #!/Library/Developer/CommandLineTools/usr/bin/python3 -W ignore

This is macOS case. Change install path to your environment accordingly.
