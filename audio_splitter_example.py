import os
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_audio(file, dest_path='./tmp'):
    try:
        os.mkdir(dest_path)
    except FileExistsError:
        shutil.rmtree(dest_path)
        os.mkdir(dest_path)

    print('\nAudio splitting...')

    sound_file = AudioSegment.from_wav(file)

    audio_chunks = split_on_silence(sound_file,
                                    min_silence_len=500,
                                    keep_silence=True,
                                    silence_thresh=-35
                                    )

    start_pos = 0
    positions = []
    for i, chunk in enumerate(audio_chunks):
        duration = chunk.duration_seconds
        end_pos = start_pos + duration
        out_file = os.path.join(dest_path, "chunk_{:03d}.wav".format(i))
        print(f"splitted : {out_file}, {start_pos:.2f} - {end_pos:.2f}")
        chunk.export(out_file, format="wav")

        positions.append((start_pos, end_pos))
        start_pos = end_pos

    return positions


if __name__ == '__main__':
    wav_file = 'sample_data/t2_0001.wav'

    split_audio(wav_file)