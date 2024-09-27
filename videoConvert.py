from converter import Converter
conv = Converter()

info = conv.probe('01_2_capture.mp4')

convert = conv.convert('01_2_capture.mp4', '01_2_capture.avi', {
    'format': 'avi',
    'audio': {
        'codec': 'aac',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'hevc',
        'width': 720,
        'height': 400,
        'fps': 25
    }})

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')