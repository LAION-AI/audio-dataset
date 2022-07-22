import os


def audio_to_flac(audio_in_path, audio_out_path, sample_rate=48000, no_log=True, segment_start:float=0, segment_end:float=None):
    log_cmd = ' -v quiet' if no_log else ''
    segment_cmd = f'-ss {segment_start} -to {segment_end}' if segment_end else ''
    os.system(
        f'ffmpeg -y -i "{audio_in_path}" -vn {log_cmd} -flags +bitexact '
        f'-ar {sample_rate} -ac 1 {segment_cmd} "{audio_out_path}"')


def audio_to_mp3(audio_in_path, audio_out_path, bit_rate='192k', no_log=True):
    log_cmd = ' -v quiet' if no_log else ''
    os.system(
        f'ffmpeg -y -i "{audio_in_path}" -vn {log_cmd}  '
        f'-b:a {bit_rate} -ac 1 "{audio_out_path}"')

def cut_audio(audio_path, start_time, end_time):
    os.system(
        f'ffmpeg -y  -ss {start_time} -i "{audio_path}" -to {end_time - start_time}  "{audio_path}"')